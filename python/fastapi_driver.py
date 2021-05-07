from fastapi import FastAPI, Request
from lib.http_utils import *
from lib.makejson import *

app = FastAPI()

# Route all possible paths here
@app.get("/")
@app.get("/{path:path}")
def root(path, req: Request):

    import traceback, json
    from fastapi.responses import Response
    #from fastapi.responses JSONResponse
    #from fastapi.encoders import jsonable_encoder

    http_request = HTTPRequest()
    http_request.host = req.headers['host'].split(':')[0]
    http_request.path = "/" + path
    http_request.query_string = dict(req.query_params)

    try:

        data = main(vars(http_request))
        #return JSONResponse(
        ##    headers = {'Cache-Control': "no-cache, no-store", 'Pragma': "no-cache"},
        ##    content =  jsonable_encoder(data)
        #)
        return Response(
            media_type = "application/json",
            headers = {'Cache-Control': "no-cache, no-store", 'Pragma': "no-cache"},
            content =  json.dumps(data, indent=2, default=str)
        )
        
    except:
        return Response(status_code = 500, content = traceback.format_exc())

