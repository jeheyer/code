from json import dumps
from urllib import parse
from asyncio import run
from webapps import *


# WSGI entry point
def application(environ, start_response):

    _ = None
    code = "200 OK"
    headers = [('Content-type', 'text/plain')]

    try:

        uri = environ.get('REQUEST_URI')
        if not uri or uri == '':
            uri = environ.get('RAW_URI', '/')
        path = uri.split('?')[0]

        query_params = {}
        if '?' in uri:
            query_params = dict(parse.parse_qsl(parse.urlsplit(uri).query))

        if "/ping" in path:
            _ = ping(environ)

        if "/mortgage" in path:
            _ = mortgage(query_params)

        if "/get_table" in path:
            db_name = path.split('/')[-2]
            db_table = path.split('/')[-1]
            _ = run(get_table(db_name, db_table))

        if "/polls/" in path:
            db_name = path.split('/')[-2]
            db_join_table = path.split('/')[-1]
            _ = run(polls(db_name, db_join_table))

        if "/graffiti/" in path:
            db_name = path.split('/')[-2]
            wall = path.split('/')[-1]
            _ = run(graffiti(db_name, wall))

        if "/geoip" in path:
            ip_list = []
            if '/' in path[6:] and not path[-1] == '/':
                ip_list = path.replace("/geoip/", "").split('/')
            if len(ip_list) < 1:
                ip_list = [ get_client_ip(environ) ]
            _ = get_geoip_info(ip_list)

        if "/getdnsservers" in path:
            token = path.split("/")[-1]
            _ = get_dns_servers(token)

        if _:
            output = dumps(_, default=str, indent=2)
            headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Cache-Control', 'no-cache, no-store'),
                ('Pragma', 'no-cache'),
                ('Content-type', 'application/json'),
                ('Content-Length', str(len(output)))
            ]
        else:
            output = "Unknown call"

    except Exception as e:

        code = "500 Internal Server Error"
        output = str(format(e))

    start_response(code, headers)
    return [output.encode('utf-8')]
