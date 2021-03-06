#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# If still running Python 2.7
from __future__ import print_function

def main():

    import os, cgi

    if not 'REQUEST_METHOD' in os.environ:
        quit("Call me via the web, please")

    output = dict(os.environ)
    form = cgi.FieldStorage()
    form_data = {}
    for key in form:
        form_data[key] = str(form[key].value)
    output.update(form_data)
    return output

if __name__ == "__main__":

    import sys, json, traceback

    sys.stderr = sys.stdout

    try:
        output = main()
        print("Content-Type: text/json; charset=UTF-8\n")
        print(json.dumps(output, indent=2))

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain\n")
        traceback.print_exc(file=sys.stdout, limit=3)

