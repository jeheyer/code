#!/usr/bin/env python3

from flask import Flask, jsonify, request
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

@app.route("/", defaults = {'path': ""})
@app.route("/<string:path>")
@app.route("/<path:path>")

def index(path):
    req_info = {
        'host': request.host.split(':')[0],
        'path': "/" + path,
        'query_string': request.args,
        'remote_addr': request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        'user_agent': request.user_agent.string
    }
    return jsonify(req_info)

if __name__ == '__main__':
    app.run()
