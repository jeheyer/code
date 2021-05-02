import sys
#sys.path.insert(0, '../lib/')
#sys.path.append('../lib')
#sys.path.append(r'/mnt/web/www/code/python/lib')
sys.path.append(r'lib')

from makejson import *
from http_utils import *

# WSGI entry point
def application(environ, start_response):

    import traceback, json

    request = vars(http_request(environ))

    response_headers = [ ('Content-type', 'text/plain') ]

    try:

        if '?' in request['path']:
            request['path'], query_string = environ.get('REQUEST_URI', '/').split('?')
            for _ in environ.get('QUERY_STRING', None).split('&'):
                [key, value] = _.split('=')
                request['query_string'][key] = value

        data = main(request)
        output = json.dumps(data, indent=2, default=str)

        response_headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(output))),
            ('Cache-Control', 'no-cache, no-store'),
            ('Pragma', 'no-cache')
        ]
        start_response('200 OK', response_headers)
        return [ output.encode('utf-8') ]

    except:

        start_response('500 Internal Server Error', response_headers)
        error = traceback.format_exc()
        return [ str(error).encode('utf-8') ]
