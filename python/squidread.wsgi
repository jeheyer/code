from squidread import *

# WSGI entry point
def application(environ, start_response):

    import traceback, json
    from random import sample

    try:

        data, reporters, client_ips, codes = GetData()
        output = json.dumps(data[0:500])
        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('Cache-Control', 'no-cache')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
