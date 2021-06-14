#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, cgi

def main():

    output = {}
 
    if 'REQUEST_METHOD' in os.environ:

        for _ in ['SERVER_PROTOCOL', 'SERVER_PORT', 'HTTP_HOST', 'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR', 'REQUEST_METHOD', 'SCRIPT_URL']:
            output[_] =  os.environ.get(_, '')
        
        form = cgi.FieldStorage()
        for key in form:
            output[key] = str(form[key].value)
        return dict(env)
    else:
        quit("Call me via the web")            

if __name__ == "__main__":

    import sys, json, traceback

    sys.stderr = sys.stdout

    try:
        output = main()
        print("Content-Type: text/json; charset=UTF-8\n")
        print(json.dumps(output, indent=2))

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain\n")
        traceback.print_exc(file=sys.stdout, limit = 3)

