#!/usr/bin/env python3

def main(request):
  
    modules = [ "mortgage", "geoip" ]

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

    import json, traceback

    try:
        request = { 
            'host': environ.get('HTTP_HOST', 'localhost'),
            'path': environ.get('REQUEST_URI', '/'),
            'query_string': {}
        }
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
            ('X-Backend-Server', 'Apache + mod_wsgi')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:
        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
