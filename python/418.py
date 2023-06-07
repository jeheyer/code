# Just a simple little WSGI app that returns a 418 code

import json
import sys
import platform
import traceback

FIELDS = {
    'request-method': "REQUEST_METHOD",
    'path': "PATH_INFO",
    'user-agent': "HTTP_USER_AGENT",
    'x-real-ip': "HTTP_X_REAL_IP",
    'via': "VIA",
    'x-forwarded-for': "HTTP_X_FORWARDED_FOR",
    'x-forwarded-proto': "HTTP_X_FORWARDED_PROTO",
    'x-forwarded-host': "HTTP_X_FORWARDED_HOST",
    'server-software': "SERVER_SOFTWARE",
    'server-port': "SERVER_PORT"
}


def get_request_info(environ={}):

    output = {
        'text': "Here is some information about your request.",
        'host': environ.get('HTTP_HOST', "localhost:80").split(":")[0],
    }
    for key, value in FIELDS.items():
        if value in environ:
            output[key] = environ.get(value)
    output['server-os'] = platform.system()
    output['server-kernel'] = platform.release()
    output['python-version'] = str(sys.version).split(" ")[0]

    return output


def application(environ, start_response):

    code = "418 I'm a teapot"
    headers = [('Content-type', 'text/plain')]

    try:

        message = json.dumps(get_request_info(environ), default=str, indent=4)
        headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(message)))
        ]

    except Exception as e:

        code = "500 Internal Server Error"
        message = str(traceback.format_exc())

    start_response(code, headers)
    return [message.encode('utf-8')]
