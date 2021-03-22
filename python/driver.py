#!/usr/bin/env python3

import sys, json

def main(request):

    modules = [ "mortgage", "geoip", "get_table" ]

    for _ in modules:

        if "mortgage" in request['path']:
            from financial import GetPaymentData
            return GetPaymentData(**request['query_string'])

        if "geoip" in request['path']:
            from geoip import GeoIP
            from ip_utils import GetClientIP
            ipv4_address = request['path'].split("/")[2]
            if not ipv4_address:
                ipv4_address = GetClientIP()
            return vars(GeoIP(ipv4_address))

        if "getdnsservers" in request['path']:
            from system_tools import GetDNSServersFromToken
            token = request['path'].split("/")[2]
            if not token:
                 token = "testing1234"
            return GetDNSServersFromToken(token)

        if "get_table" in request['path']:
            from system_tools import GetDNSServersFromToken
            token = request['path'].split("/")[2]
            if not token:
                 token = "testing1234"
            return GetDNSServersFromToken(token)

    return dict(available_modules = modules)

# Old School CGI Entry Point
def ParseCGI():
 
    import os, cgi

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

    import os, traceback

    sys.stderr = sys.stdout

    try:
        if os.environ.get('REQUEST_METHOD'):
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

# AWS Lambda Entry Point
def lambda_handler(event, context):

    try:

        request = {
            'host': event['headers']['host'],
            'path': event['path'],
            'headers': {},
            'query_string': event['queryStringParameters']
        }

        data = main(request)

    except Exception as e:
         headers = { 'Content-Type': "text/plain" }
         return  {'statusCode': 500, 'headers': headers, 'body': format(e)}

    return {
        'statusCode': 200,
        'headers': { 'Content-Type': "application/json" },
        'body': json.dumps(data, sort_keys=True, indent=2)
    }


# WSGI entry point
def application(environ, start_response):

    import traceback

    request = { 
        'host': environ.get('HTTP_HOST', 'localhost'),
        'path': environ.get('REQUEST_URI', '/'),
        'query_string': {}
    }

    try:

        if '?' in request['path']:
            request['path'], query_string = environ.get('REQUEST_URI', '/').split('?')
            for _ in environ.get('QUERY_STRING', None).split('&'):
                [key, value] = _.split('=')
                request['query_string'][key] = value

        data = main(request)
        output = json.dumps(data, sort_keys=True, indent=2)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('X-Backend-Server', 'WSGI')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
