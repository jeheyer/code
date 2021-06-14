#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, cgi

def main():

    output = {}
 
    if 'REQUEST_METHOD' in os.environ:

        for _ in ['SERVER_PROTOCOL', 'SERVER_PORT', 'HTTP_HOST', 'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR', 'REQUEST_METHOD', 'SCRIPT_URL']:
            output[_] =  os.environ.get(_, '')
        
        query_params = {}
        if os.environ.get('REQUEST_METHOD') == "POST":
            for key in form:
                query_params[key] = str(form[key].value)
        else:
            query_params = dict(cgi.FieldStorage())
    else:
        quit("Call me via the web")            

if __name__ == "__main__":

    import sys, json, traceback

    sys.stderr = sys.stdout

    try:
        output = main()
        print("Content-Type: text/json; charset=UTF-8\n")
        print(json.dumps(output))

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain\n")
        traceback.print_exc(file=sys.stdout, limit = 3)

