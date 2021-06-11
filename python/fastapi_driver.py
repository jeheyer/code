#!/usr/bin/env python3

from fastapi import FastAPI, Request
from lib.http_utils import *
from lib.makejson import *

app = FastAPI()

# Route all possible paths here
@app.get("/")
@app.get("/{path:path}")
def root(path, req: Request):

    from fastapi.responses import Response, JSONResponse
    from fastapi.encoders import jsonable_encoder
    import traceback

    http_request = HTTPRequest()
    http_request.host = req.headers['host'].split(':')[0]
    http_request.path = "/" + path
    http_request.query_string = dict(req.query_params)
    if 'x-real-ip' in req.headers:
        http_request.client_ip = req.headers['x-real-ip']
    else:
        http_request.client_ip = req.client.host

    try:

        data = main(vars(http_request))
        return JSONResponse(
            headers = {'Cache-Control': "no-cache, no-store", 'Pragma': "no-cache"},
            content =  jsonable_encoder(data)
        )
        #return Response(
        #    media_type = "application/json",
        #    headers = {'Cache-Control': "no-cache, no-store", 'Pragma': "no-cache"},
        #    content =  json.dumps(data, default=str)
        #)

    except:
        return Response(status_code = 500, content = traceback.format_exc())
