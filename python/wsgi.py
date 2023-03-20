from flask import Flask, request, jsonify, redirect, Response
from lib.webapps import *
import asyncio

app = Flask(__name__)


@app.route("/ping")
def _ping():

    try:
        data = ping(request.environ)
        return jsonify(data)
    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/mortgage")
def _mortgage():

    try:
        data = mortgage(request.args)
        return jsonify(data)
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


@app.route("/graffiti_post", methods=["POST"])
def _graffiti_post():

    try:
        db_name = request.form.get('db_name')
        wall = request.form.get('wall')
        graffiti_url = request.form.get('graffiti_url')
        name = request.form.get('name')
        text = request.form.get('text')
        db_name = "primus"
        wall = "Brain"
        redirect_url = asyncio.run(graffiti_post(db_name, wall, graffiti_url, name, text))
        return redirect(redirect_url, code=302)

    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/poll_vote", methods=["POST"])
def _poll_vote():

    try:
        db_name = request.form.get('poll_db')
        poll_name = request.form.get('poll_name')
        poll_url = request.form.get('poll_url')
        poll_desc = request.form.get('poll_desc', "")
        choice_id = request.form.get('choice_id')

        redirect_url = poll_vote(db_name, poll_name, poll_url, poll_desc, choice_id)
        return redirect(redirect_url, code=302)

    except Exception as e:
        return Response(format(e), 500, content_type="text/plain")


@app.route("/geoip", methods=["GET"])
@app.route("/geoip/", methods=["GET"])
@app.route("/geoip/<path:path>", methods=["GET"], defaults={"path": ""})
def _geoip(path=None):

    try:
        if not path:
            ip_list = [get_client_ip(request.environ)]
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
