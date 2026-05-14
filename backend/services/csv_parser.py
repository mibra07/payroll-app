# services/csv_parser.py
import csv # csv is used to read and write CSV files, it is imported from the standard library
from io import StringIO # StringIO is used to create an in-memory file-like object, it is imported from the standard library

async def parse_csv(file): # parse_csv is an asynchronous function that takes a file as input and returns a list of dictionaries representing the rows in the CSV file
    content = await file.read() # read the content of the file asynchronously
    print("File size", len(content))
    csv_data = StringIO(content.decode('utf-8')) # decode the content from bytes to a string using UTF-8 encoding and create an in-memory file-like object
    return csv.DictReader(csv_data) # return a DictReader object that can be used to iterate over the rows in the CSV file as dictionaries