
from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from lib.webapps import *

RESPONSE_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': "no-cache, no-store",
    'Pragma': "no-cache"
}

app = FastAPI()


@app.get("/ping")
def _ping(req: Request):

    try:
        #print(vars(req))
        data = ping({'header-name': "header-value"})
        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return Response(status_code=500, content=format(e))


@app.get("/mortgage")
def _mortgage(req: Request):

    try:
        data = mortgage(dict(req.query_params))
        return JSONResponse(content=jsonable_encoder(data))
    except Exception as e:
        return Response(status_code=500, content=format(e))


@app.get("/get_table/{db_name}/{db_table}")
@app.get("/graffiti/{db_name}/{wall}")
@app.get("/polls/{db_name}/{db_join_table}")
def _get_table(db_name, db_table = None, wall = None, db_join_table = None, req: Request = None):

    try:

        path = req.url.path
        if path.startswith("/polls"):
            data = get_table(db_name, "polls", db_join_table=db_join_table)
        elif path.startswith("/graffiti"):
            data = get_table(db_name, "graffiti", wall=wall)
        else:
            data = get_table(db_name, db_table)

        return JSONResponse(headers=RESPONSE_HEADERS, content=jsonable_encoder(data))

    except Exception as e:
        return Response(status_code=500, content=format(e))

@app.post("/graffiti_post")
async def _graffiti_post(
    db_name: str = Form(...),
    wall: str = Form(...),
    graffiti_url: str = Form(...),
    name: Optional[str] = Form("Anonymous Coward"),
    text: Optional[str] = Form("I have nothing to say"),
):

    try:
        redirect_url = graffiti_post(db_name, wall, graffiti_url, name, text)
        return RedirectResponse(url=redirect_url, status_code=302)

    except:
        return Response(status_code=500, content=format(e))

@app.get("/poll_vote")
async def poll_vote(
    poll_name: str = Form(...),
    poll_url: str = Form(...),
    poll_description: Optional[str] = Form("")
):

    try:
        redirect_url = f"{poll_url}?poll_name={poll_name}&poll_desc={poll_desc}"
        return RedirectResponse(url = redirect_url, status_code = 302)

    except Exception as e:
        return Response(status_code=500, content=format(e))

@app.post("/poll_vote")
async def poll_vote(
    poll_db: str = Form(...),
    poll_name: str = Form(...),
    poll_url: str = Form(...),
    poll_desc: Optional[str] = Form("")
):

    try:
        PollVote(poll_db, poll_name, choice_id)
        redirect_url = f"{poll_url}?poll_name={poll_name}&poll_desc={poll_desc}"
        return RedirectResponse(url=redirect_url, status_code=302)

    except Exception as e:
        return Response(status_code=500, content=format(e))

@app.get("/geoip/{ip_list}")
def _geoip(ip_list):

    try:
        ip_list = ip_list.split('/')
        data = get_geoip_info(ip_list)
        return JSONResponse(headers=RESPONSE_HEADERS, content=jsonable_encoder(data))

    except Exception as e:
        return Response(status_code=500, content=format(e))

@app.get("/getdnsservers/{token}")
def _getdnsservers(token):

    try:
        data = get_dns_servers(token)
        return JSONResponse(headers=RESPONSE_HEADERS, content=jsonable_encoder(data))

    except Exception as e:
        return Response(status_code=500, content=format(e))
