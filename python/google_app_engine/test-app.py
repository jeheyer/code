#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route("/")
def ShowRequest():

    import traceback, jsonpickle

    try:
        return jsonify(jsonpickle.encode(request)), 200

    except:
        return format(traceback.format_exc()), 500, {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()
