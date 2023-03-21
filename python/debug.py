def application(environ, start_response):

    from json import dumps

    code = "200 OK"
    headers = [('Content-type', 'text/plain')]

    try:

        data = {
           'remote_addr': environ.get('REMOTE_ADDR'),
           'x_real_ip': environ.get('HTTP_X_REAL_IP'),
           'x_forwarded_for': environ.get('HTTP_X_FORWARDED_FOR'),
           'x_forwarded_proto': environ.get('HTTP_X_FORWARDED_PROTO'),
        }
        output = dumps(data, default=str, indent=2)

    except Exception as e:

        code = "500 Internal Server Error"
        output = str(format(e))

    start_response(code, headers)
    return [output.encode('utf-8')]
