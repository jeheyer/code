from quart import Quart, request, Response, jsonify
from asyncio import create_task
from webapps import *


app = Quart(__name__)


@app.route("/ping")
def _ping():

    try:
        _ = ping(request=request)
        return jsonify(_)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/mortgage")
def _mortgage():

    try:
        _ = mortgage(request.args)
        return jsonify(_)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/get_table/<db_name>/<db_table>")
async def _get_table(db_name, db_table=None):

    try:
        _ = await create_task(get_table(db_name, db_table))
        return jsonify(_)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/graffiti/<db_name>/<wall>")
async def _graffiti(db_name, wall):

    try:
        _ = await create_task(graffiti(db_name, wall))
        return jsonify(_)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/polls/<db_name>/<db_join_table>")
async def _polls(db_name, db_join_table):
    try:
        _ = await create_task(polls(db_name, db_join_table))
        return jsonify(_)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/geoip")
@app.route("/geoip/")
@app.route("/geoip/<path:path>")
def _geoip(path=None):

    try:
        if not path:
            request_headers = {
                'http_x_real_ip': request.headers.get('X-Real-IP'),
                'http_x_forwarded_for': request.headers.get('X-Forwarded-For'),
                'remote_addr': request.remote_addr,
            }
            ip_list = [get_client_ip(request_headers)]
        else:
            if '/' in path:
                ip_list = path.split('/')
            else:
                ip_list = [path]
        _ = get_geoip_info(ip_list)
        return jsonify(_)

    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
