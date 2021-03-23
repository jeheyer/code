#!/usr/bin/env python

from makerest import *
import sys, os, json

# Old School CGI Entry Point
def ParseCGI():
 
    import cgi

    request = {
        'host': os.environ.get('HTTP_HOST', 'localhost'),
        'path': os.environ.get('REQUEST_URI', '/').split('?')[0],
        'query_string': {}
    }

    query_fields_objects = cgi.FieldStorage()

    for key in query_fields_objects:
        value = query_fields_objects[key].value
        request['query_string'][key] = str(value)

    return request

# Called via CLI
def ParseCLI():

    request = dict(host = "localhost", path = "/", query_string = {})

    # Use argument, if provided, to simulate HTTP Path and query string
    if len(sys.argv) > 1:
       request['path'] = sys.argv[1]
       if '?' in request['path']:
            request['path'], query_string = request['path'].split('?')
            for _ in query_string.split('&'):
                [key, value] = _.split('=')
                request['query_string'][key] = value

    return request

# Primary entry point
if __name__ == '__main__':

    import traceback

    sys.stderr = sys.stdout

    try:
        if 'REQUEST_METHOD' in os.environ:
            request = ParseCGI()
        else:
            request = ParseCLI()

        data = main(request)
        output = json.dumps(data, sort_keys=True, indent=2)

        print("Content-Length: {}".format(len(output)))
        print("Content-Type: application/json; charset=UTF-8\n")
        print(output)

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)
