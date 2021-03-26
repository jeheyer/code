from makejson import *

# WSGI entry point
def application(environ, start_response):

    import traceback, json

    request = {  
        'host': environ.get('HTTP_HOST', 'localhost'),
        'path': environ.get('REQUEST_URI', '/'),
        'query_string': {},
        'client_ip': environ.get('HTTP_X_REAL_IP', None)
    }
  
    try:

        if not request['client_ip']:
            request['client_ip'] = environ['REMOTE_ADDR']

        if '?' in request['path']:
            request['path'], query_string = environ.get('REQUEST_URI', '/').split('?')
            for _ in environ.get('QUERY_STRING', None).split('&'):
                [key, value] = _.split('=')
                request['query_string'][key] = value

        data = main(request)
        output = json.dumps(data, indent=2)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('X-Backend-Server', 'WSGI'),
            ('Cache-Control', 'no-cache, no-store'),
            ('Pragma', 'no-cache')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
