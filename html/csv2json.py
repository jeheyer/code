#!/usr/bin/env python3

def ReadCSV(file_name: str):

    import csv

    # Read CSV
    file = open(file_name)
    csvreader = csv.reader(file)

    # Get Headers
    header_fields = []
    header_fields = next(csvreader)

    # Get data
    rows = []
    for _ in csvreader:
        rows.append(_)
    file.close()

    return header_fields, rows

def FormatData(header_fields: list, data: list):

    json_data = []

    for _ in range(len(data)):
       row = {}
       row['name'] = data[_][0]
       for i in range(1,len(data[_])):
           row[header_fields[i]] = data[_][i]
       json_data.append(row)

    return json_data

def main():

    import sys, json

    if len(sys.argv) > 1:
        CSV_FILE = sys.argv[1]
    else:
        sys.exit("Usage: " + sys.argv[0] + " <CSV_FILE_LOCATION>")
    
    headers, data = ReadCSV(CSV_FILE)
    print(json.dumps(FormatData(headers, data), indent=2))

if __name__ == "__main__":
    main()
