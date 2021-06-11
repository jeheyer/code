#!/usr/bin/env python3

from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import RedirectResponse
from typing import Optional
from lib.http_utils import *
from lib.makejson import *
from lib.web_apps import *
import traceback

app = FastAPI()

# Route all possible paths here
@app.get("/{path:path}")
def get_handler(path, req: Request):

    from fastapi.responses import JSONResponse
    from fastapi.encoders import jsonable_encoder

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

    except:
        return Response(status_code = 500, content = traceback.format_exc())

@app.post("/graffiti_post")
async def graffiti_post(
    db_name: str = Form(...),
    wall: str = Form(...),
    graffiti_url: str = Form(...),
    name: Optional[str] = Form("Anonymous Coward"),
    text: Optional[str] = Form("I have nothing to say"),
):

    try:
        GraffitiPost(db_name, wall, name, text)
        redirect_url = f"{graffiti_url}?wall={wall}"
        return RedirectResponse(url = redirect_url, status_code = 302)

    except:
        return Response(status_code = 500, content = traceback.format_exc())

@app.get("/poll_vote")
async def poll_vote(
    poll_name: str = Form(...),
    poll_url: str = Form(...),
    poll_description: Optional[str] = Form("")
):

    try:
        redirect_url = f"{poll_url}?poll_name={poll_name}&poll_desc={poll_desc}"
        return RedirectResponse(url = redirect_url, status_code = 302)

    except:
        return Response(status_code = 500, content = traceback.format_exc())

@app.post("/poll_vote")
async def poll_vote(
    poll_db: str = Form(...),
    poll_name: str = Form(...),
    poll_url: str = Form(...),
    poll_description: Optional[str] = Form("")
):

    try:
        PollVote(poll_db, poll_name, choice_id)
        redirect_url = f"{poll_url}?poll_name={poll_name}&poll_desc={poll_desc}"
        return RedirectResponse(url = redirect_url, status_code = 302)

    except:
        return Response(status_code = 500, content = traceback.format_exc())