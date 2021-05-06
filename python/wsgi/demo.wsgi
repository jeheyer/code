def application(environ, start_response):

    from urllib import parse

    server_host = environ.get('HTTP_HOST', 'localhost')
    server_port = environ.get('SERVER_PORT', 80)
    path = environ.get('REQUEST_URI', '/').split('?')[0]
    query_params = dict(parse.parse_qsl(parse.urlsplit(environ['REQUEST_URI']).query))
