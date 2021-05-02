#!/usr/bin/env python3

def application(environ, start_response):

    import json, traceback

    try:
        request = {
            'host': environ.get('HTTP_HOST', 'localhost'),
            'path': environ.get('REQUEST_URI', '/').split('?')[0]
        }
        data = [
            {'name': "Tom",   'age': 22},
            {'name': "Harry", 'age': 33},
            {'name': "Dick",  'age': 44}
        ]
        json_output = json.dumps(data, sort_keys=True, indent=2)
        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(json_output)))
        ]
        start_response('200 OK', response_headers)
        return [ data_as_json.encode('utf-8') ]

    except:
        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]

