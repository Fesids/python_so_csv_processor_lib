import csv
import sys
from typing import List, Dict

def process_csv(data: str, selected_columns: str, row_filter_definitions: str) -> str:
    if selected_columns:
        selected_columns = selected_columns.split(',')
    else:
        selected_columns = []

    row_filters = parse_filters(row_filter_definitions)
    reader = csv.DictReader(data.splitlines())
    all_columns = reader.fieldnames

    if not selected_columns:
        selected_columns = all_columns

    for col in selected_columns:
        if col not in all_columns:
            sys.stderr.write(f"Header '{col}' not found in CSV file/string\n")
            sys.exit(1)

    for filter in row_filters:
        if filter['col'] not in all_columns:
            sys.stderr.write(f"Header '{filter['col']}' not found in CSV file/string\n")
            sys.exit(1)

    result = [selected_columns]
    for row in reader:
        if all(apply_filter(row, f) for f in row_filters):
            result.append([row[col] for col in selected_columns])

    return '\n'.join([','.join(row) for row in result])

def parse_filters(definitions: str) -> List[Dict]:
    filters = []
    for definition in definitions.split('\n'):
        if definition.strip():
            for op in ['!=', '>=', '<=', '=', '>', '<']:
                if op in definition:
                    col, value = definition.split(op)
                    filters.append({'col': col.strip(), 'condition': op, 'value': value.strip()})
                    break
            else:
                sys.stderr.write(f"Invalid filter: '{definition}'\n")
                sys.exit(1)
    return filters

def apply_filter(row: Dict[str, str], f: Dict) -> bool:
    col = f['col']
    value = row[col]
    if f['condition'] == '=':
        return value == f['value']
    elif f['condition'] == '!=':
        return value != f['value']
    elif f['condition'] == '>':
        return float(value) > float(f['value'])
    elif f['condition'] == '>=':
        return float(value) >= float(f['value'])
    elif f['condition'] == '<':
        return float(value) < float(f['value'])
    elif f['condition'] == '<=':
        return float(value) <= float(f['value'])
    return False

def process_csv_file(file_path: str, selected_columns: str, row_filter_definitions: str, output_file_path: str) -> str:
    with open(file_path, 'r') as file:
        data = file.read()
    #return process_csv(data, selected_columns, row_filter_definitions)
    #return process_csv(data, teste_columns)
    processed_data = process_csv(data, selected_columns, row_filter_definitions)
    with open(output_file_path, 'w') as file:
        file.write(processed_data)

# Chamar a função para processar o arquivo CSV
process_csv_file("../data_header.csv", "header1,header3", "header1!=0\nheader3>1", "output.csv")

# Exportar a função usando ctypes
# python setup.py build_ext --inplace compilar a biblioteca para .so
from ctypes import c_char_p, CFUNCTYPE

def create_shared_lib():
    def process_csv_file_ctypes(file_path: c_char_p, selected_columns: c_char_p, row_filter_definitions: c_char_p) -> None:
        process_csv_file(file_path.decode('utf-8'), selected_columns.decode('utf-8'), row_filter_definitions.decode('utf-8'))

    ProcessCsvFileFunc = CFUNCTYPE(None, c_char_p, c_char_p, c_char_p)
    process_csv_file_ctypes_c = ProcessCsvFileFunc(process_csv_file_ctypes)
    return process_csv_file_ctypes_c

shared_lib = create_shared_lib()
