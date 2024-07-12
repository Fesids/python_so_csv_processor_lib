import unittest
import io
import sys

from index import process_csv

class TestCSVProcessor(unittest.TestCase):
    def setUp(self):
        self.csv_data = """header1,header2,header3
1,2,3
4,5,6
7,8,9"""
    
    def test_process_csv_all_columns(self):
        expected_output = """header1,header2,header3
1,2,3
4,5,6
7,8,9"""
        result = process_csv(self.csv_data, "", "")
        self.assertEqual(result, expected_output)
    
    def test_process_csv_selected_columns(self):
        expected_output = """header3,header1
3,1
6,4
9,7"""
        result = process_csv(self.csv_data, "header3,header1", "")
        self.assertEqual(result, expected_output)
    
    def test_process_csv_with_filters(self):
        expected_output = """header1,header3
4,6"""
        result = process_csv(self.csv_data, "header1,header3", "header1=4\nheader3<7")
        self.assertEqual(result, expected_output)
    
    def test_process_csv_nonexistent_column(self):
        captured_output = io.StringIO()
        sys.stderr = captured_output
        with self.assertRaises(SystemExit):
            process_csv(self.csv_data, "header4", "")
        self.assertIn("Header 'header4' not found in CSV file/string", captured_output.getvalue())
    
    def test_process_csv_invalid_filter(self):
        captured_output = io.StringIO()
        sys.stderr = captured_output
        with self.assertRaises(SystemExit):
            process_csv(self.csv_data, "header1,header3", "header1#2")
        self.assertIn("Invalid filter: 'header1#2'", captured_output.getvalue())
    
    def tearDown(self):
        sys.stderr = sys.__stderr__

if __name__ == "__main__":
    unittest.main()
