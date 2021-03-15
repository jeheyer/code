#!/usr/bin/env python

import sys, json

def main(request):

    modules = [ "mortgage", "geoip" ]

    sys.path.insert(1, 'lib/')

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

    return dict(available_modules = modules)

# Traditional CGI Entry Point
def ParseCGI():
 
    import cgi

    http_request = {
        'host': os.environ.get('HTTP_HOST', 'localhost'),
        'path': os.environ.get('REQUEST_URI', '/').split('?')[0],
        'query_string': {}
    }

    query_fields_objects = cgi.FieldStorage()

    for key in query_fields_objects:
        value = query_fields_objects[key].value
        http_request['query_string'][key] = str(value)

    return http_request

def ParseCLI():

   request = dict(host = "localhost", path = "/")

   if len(sys.argv) > 1:
       request['path'] = sys.argv[1]

   return request

# Primary entry point
if __name__ == '__main__':

    import traceback, os

    sys.stderr = sys.stdout

    try:
        if os.environ.get('REQUEST_METHOD'):
            request = ParseCGI()
        else:
            request = ParseCLI()

        data = main(request)

        print("Content-Type: application/json; charset=UTF-8\n")
        print(json.dumps((data), indent=3))

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit = 3)

# AWS Lambda Entry Point
def lambda_handler(event, context):

    http_request = {
        'host': event['headers']['host'],
        'path': event['path'],
        'headers': {},
        'query_string': event['queryStringParameters']
    }

    try:
        data = main(http_request)

    except Exception as e:
         headers = { 'Content-Type': "text/plain" }
         return  {'statusCode': 500, 'headers': headers, 'body': format(e)}

    headers = { 'Content-Type': "application/json" }
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(data)}

