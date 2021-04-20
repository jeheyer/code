#!/usr/bin/env python3

from flask import Flask, jsonify, request
##from flask import jsonify
#from flask import request 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/<path>')

def index(path):
    host = request.host.split(':')[0]
    path = "/" + path
    query_string = request.args
    d = {'host': host, 'path': path, 'query_string': query_string}
    return jsonify(d)

if __name__ == '__main__':
    app.run()
