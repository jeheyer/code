#!/usr/bin/env python3

from fastapi import FastAPI, Request

app = FastAPI()

# Route all possible paths here
@app.get("/")
@app.get("/{path:path}")
def root(path, req: Request):

    import traceback
    from starlette.responses import Response

    [host, port] = req.headers['host'].split(':')
    path = "/" + path    
    query_string = dict(req.query_params)

    try:

        http_request = dict(host = host, port = port, p = path , qs = query_string)
        return Response(
            status_code = 200,
            headers = {'Content-type': "text/plain"},
            content = str(http_request)
        )
        
    except:
        return Response(status_code = 500, content = traceback.format_exc())

