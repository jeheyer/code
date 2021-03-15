#!/usr/bin/env python3

import json
import csv
import xml

def ReadInput(file_name: str) -> (list, str):

    lines = []
    
    f = open(file_name)
    lines = f.readlines()

    file_ext = file_name.split(".")[-1]

    return (lines, file_ext)

def ConvertToDict(contents: list, file_type: str) -> list:
    
    data = []
    
    if file_type == "csv":
        
        for line in contents:
            line = line.rstrip()
            print(line)
            parts = line.split(",")
            obj = {}
            for i in range(0,len(parts)):
                obj[i] = parts[i]
            data.append(obj)
            
    return data
    
    
def main():
    data, file_type = ReadInput("test.csv")
    return ConvertToDict(data, "csv")

if __name__ == '__main__':

    import sys, os, traceback, time

    sys.stderr = sys.stdout

    start_time = time.time()

    try:
        output = main()
        if 'REQUEST_METHOD' in os.environ:
            print("Content-Type: text/json; charset=UTF-8\n")
        print(json.dumps(output, indent=3))

    except Exception as e:
        
        if 'REQUEST_METHOD' in os.environ:
            print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit = 3)