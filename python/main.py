from json import dumps
from urllib import parse
from webapps import *
import asyncio


# WSGI entry point
def application(environ, start_response):

    data = None
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
            data = ping(environ)

        if "/mortgage" in path:
            data = mortgage(query_params)

        if "/get_table" in path:
            db_name = path.split('/')[-2]
            db_table = path.split('/')[-1]
            data = asyncio.run(get_table(db_name, db_table))

        if "/polls" in path:
            db_name = path.split('/')[-2]
            db_join_table = path.split('/')[-1]
            data = asyncio.run(get_table(db_name, "polls", db_join_table=db_join_table))

        if "/graffiti/" in path:
            db_name = path.split('/')[-2]
            wall = path.split('/')[-1]
            data = asyncio.run(get_table(db_name, "graffiti", wall=wall))

        if "/geoip" in path:
            ip_list = []
            if '/' in path[6:] and not path[-1] == '/':
                ip_list = path.replace("/geoip/", "").split('/')
            if len(ip_list) < 1:
                ip_list = [ get_client_ip(environ) ]
            data = get_geoip_info(ip_list)

        if "/getdnsservers" in path:
            token = path.split("/")[-1]
            data = get_dns_servers(token)

        if data:
            output = dumps(data, default=str, indent=2)
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
