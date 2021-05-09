#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def ShowRequest():

    import traceback

    try:
        return str(vars(request)), 200, {'Content-Type': "text/plain"}

    except:
        return format(traceback.format_exc()), 500, {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run()
