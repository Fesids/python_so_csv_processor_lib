from setuptools import setup, Extension

module = Extension('csv_processor', sources=['index.py'])

setup(
    name='csv_processor',
    version='1.0',
    description='CSV Processor Module',
    ext_modules=[module]
)
