from quart import Quart, request, Response, jsonify
from webapps import *
import asyncio

app = Quart(__name__)


@app.route("/ping")
def _ping():

    try:
        data = ping(request=request)
        return jsonify(data)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/mortgage")
def _mortgage():

    try:
        data = mortgage(request.args)
        return data
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/get_table/<db_name>/<db_table>")
@app.route("/graffiti/<db_name>/<wall>")
@app.route("/polls/<db_name>/<db_join_table>")
def _get_table(db_name, db_table=None, wall=None, db_join_table=None):

    try:
        path = request.path
        if path.startswith("/polls"):
            data = asyncio.run(get_table(db_name, "polls", db_join_table=db_join_table))
        elif path.startswith("/graffiti"):
            data = asyncio.run(get_table(db_name, "graffiti", wall=wall))
        else:
            data = asyncio.run(get_table(db_name, db_table))
        return jsonify(data)

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
        data = get_geoip_info(ip_list)
        return jsonify(data)

    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
