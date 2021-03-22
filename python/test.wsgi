#!/usr/bin/env python3

import sys, json, traceback

def main(request):

    modules = [ "mortgage", "geoip" ]

    #sys.path.insert(1, 'lib')

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

def application(environ, start_response):

    try:
        http_request = {
            'host': environ.get('HTTP_HOST', 'localhost'),
            'path': environ.get('REQUEST_URI', '/').split('?')[0],
            'query_string': {}
        }
        data = main(http_request)
        data_as_json = json.dumps(data, sort_keys=True, indent=2)
        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(data_as_json)))
        ]
        start_response('200 OK', response_headers)
        output = data_as_json.encode('utf-8')
        return [output]

    except:
        start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
        error = traceback.format_exc()
        return [str(error).encode('utf-8')]
