from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from asyncio import create_task
from webapps import *

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


async def _get_table(req: Request):

    try:
        db_name = req.path_params.get('db_name')
        db_table = req.path_params.get('db_table')
        data = await create_task(get_table(db_name, db_table))
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


async def _graffiti(req: Request):

    try:

        db_name = req.path_params.get('db_name')
        wall = req.path_params.get('wall')
        data = await create_task(graffiti(db_name, wall))
        formatted_data = []
        for row in data:
            formatted_data.append({
                'timestamp': row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'name': row['name'],
                'text': row['text'],
            })
        data = formatted_data
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)

    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


async def _graffiti_post(req: Request):

    try:
        inputs = await req.form()
        db_name = inputs['db_name']
        wall = inputs['wall']
        graffiti_url = inputs.get('graffiti_url')
        name = inputs.get('name')
        text = inputs.get('text')
        redirect_url = await create_task(graffiti_post(db_name, wall, graffiti_url, name, text))
        return RedirectResponse(url=redirect_url, status_code=302)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


async def _polls(req: Request):

    try:
        db_name = req.path_params.get('db_name')
        db_join_table = req.path_params.get('db_join_table')
        data = await create_task(polls(db_name, db_join_table=db_join_table))
        return JSONResponse(content=data, headers=RESPONSE_HEADERS)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


async def _poll_vote(req: Request):

    try:
        inputs = await req.form()
        db_name = inputs['db_name']
        poll_name = inputs['poll_name']
        poll_url = inputs.get('poll_url')
        poll_desc = inputs.get('poll_desc', "")
        choice_id = inputs.get('choice_id', 0)
        redirect_url = await create_task(poll_vote(db_name, poll_name, poll_url, poll_desc, choice_id))
        return RedirectResponse(url=redirect_url, status_code=302)
    except Exception as e:
        return PlainTextResponse(content=format(e), status_code=500)


APP_ROUTES = [
    Route('/ping', _ping, methods=["GET", "POST"]),
    Route('/mortgage', _mortgage, methods=["GET"]),
    Route('/geoip', _geoip, methods=["GET"]),
    Route('/geoip/', _geoip, methods=["GET"]),
    Route('/geoip/{ip_list:path}', _geoip, methods=["GET"]),
    Route('/getdnsservers/{token:str}', _get_dns_servers, methods=["GET"]),
    Route('/get_table/{db_name:str}/{db_table:str}', _get_table,  methods=["GET"]),
    Route('/graffiti/{db_name:str}/{wall:str}', _graffiti,  methods=["GET"]),
    Route('/graffiti_post', _graffiti_post,  methods=["POST"]),
    Route('/polls/{db_name:str}/{db_join_table:str}', _polls,  methods=["GET"]),
    Route('/poll_vote', _poll_vote,  methods=["GET", "POST"]),
]

app = Starlette(debug=True, routes=APP_ROUTES)

if __name__ == '__main__':

    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)

