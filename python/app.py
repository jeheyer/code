from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from typing import Optional
from traceback import format_exc
from webapps import *
import asyncio

RESPONSE_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': "no-cache, no-store",
    'Pragma': "no-cache"
}


def _ping(req: Request):

    try:
        data = ping(request=req)
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


def _mortgage(req: Request):

    try:
        data = mortgage(dict(req.query_params))
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


def _geoip(req: Request):

    try:
        ip_list = req.path_params.get('ip_list')
        if not ip_list:
            request_headers = {
                'http_x_real_ip': req.headers.get('X-Real-IP'),
                'http_x_forwarded_for': req.headers.get('X-Forwarded-For'),
                'remote_addr': req.client.host
            }
            ip_list = [get_client_ip(request_headers)]
        else:
            if '/' in ip_list:
                ip_list = ip_list.split('/')
            else:
                ip_list = [ip_list]
        data = get_geoip_info(ip_list)
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


def _get_dns_servers(req: Request):

    try:
        token = req.path_params.get('token')
        data = get_dns_servers(token)
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


def _get_table(req: Request):

    try:

        path = req.url.path
        db_name = req.path_params.get('db_name')
        db_table = req.path_params.get('db_table')
        db_join_table = req.path_params.get('db_join_table')
        wall = req.path_params.get('wall')
        if path.startswith("/polls"):
            data = asyncio.run(get_table(db_name, "polls", db_join_table=db_join_table))
        elif path.startswith("/graffiti"):
            data = asyncio.run(get_table(db_name, "graffiti", wall=wall))
        else:
            data = asyncio.run(get_table(db_name, db_table))
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)

    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


def _graffiti_post(req: Request):

    try:
        form = req.form()
        db_name = form['db_name']
        wall = form['wall']
        graffiti_url = form.get('graffiti_url')
        name = form.get('name')
        text = form.get('text')
        redirect_url = asyncio.run(graffiti_post(db_name, wall, graffiti_url, name, text))
        return RedirectResponse(url=redirect_url, status_code=302)

    except Exception as e:
        return PlainTextResponse(content=format_exc(), status_code=500)


def _poll_vote(req: Request):

    try:
        db_name = "primus"
        poll_name = "albums"
        poll_url = ""
        poll_desc = ""
        choice_id = 1
        poll_vote(db_name, poll_name, poll_url, poll_desc, choice_id)
    except Exception as e:
        return PlainTextResponse(content=format_exc(), status_code=500)


APP_ROUTES = [
    Route('/ping', _ping, methods=["GET", "POST"]),
    Route('/mortgage', _mortgage, methods=["GET"]),
    Route('/geoip', _geoip, methods=["GET"]),
    Route('/geoip/', _geoip, methods=["GET"]),
    Route('/geoip/{ip_list:path}', _geoip, methods=["GET"]),
    Route('/getdnsservers/{token:str}', _get_dns_servers, methods=["GET"]),
    Route('/get_table/{db_name:str}/{db_table:str}', _get_table,  methods=["GET"]),
    Route('/graffiti/{db_name:str}/{wall:str}', _get_table,  methods=["GET"]),
    Route('/graffiti_post', _graffiti_post,  methods=["POST"]),
    Route('/polls/{db_name:str}/{db_join_table:str}', _get_table,  methods=["GET"]),
    Route('/poll_vote', _poll_vote,  methods=["POST"]),
]

app = Starlette(debug=True, routes=APP_ROUTES)

if __name__ == '__main__':

    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)

