#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from paste import request
from flask import Flask, request, redirect
from lib.web_apps import *

# WSGI entry point
def application(environ, start_response):

    import traceback

    try:
        path = environ.get('REQUEST_URI', '/').split('?')[0]
        inputs = {}
        if "poll_vote" in path:
            fields = request.parse_formvars(environ)
            for _ in ['poll_db','poll_name','poll_desc','poll_url','choice_id']:
                inputs[_] = fields.get(_, None)
            if inputs['choice_id']:
                PollVote(inputs['poll_db'], inputs['poll_name'], inputs['choice_id'])
            redirect_url = f"{inputs['poll_url']}?poll_name={inputs['poll_name']}&poll_desc={inputs['poll_desc']}"

        if "graffiti_post" in path:
            fields = request.parse_formvars(environ)
            for _ in ['db_name','wall','name','text','graffiti_url']:
                inputs[_] = fields.get(_, None)
            GraffitiPost(inputs['db_name'], inputs['wall'], inputs['name'], inputs['text'])
            redirect_url = f"{inputs['graffiti_url']}?wall={inputs['wall']}"

        start_response(302, ('Location', redirect_url))
        return []

    except:

        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        return [ str(traceback.format_exc()).encode('utf-8') ]

# Flask entry point
app = Flask(__name__)

@app.route("/", defaults = {'path': ""}, methods=['POST'])
@app.route("/<string:path>", methods=['POST'])
@app.route("/<path:path>", methods=['POST'])

def root(path):

    import traceback

    try:

        inputs = {}
        if "poll_vote" in path:
            for _ in ['poll_db','poll_name','poll_desc','poll_url','choice_id']:
                inputs[_] = request.form.get(_)
            PollVote(inputs['poll_db'], inputs['poll_name'], inputs['choice_id'])
            redirect_url = f"{inputs['poll_url']}?poll_name={inputs['poll_name']}&poll_desc={inputs['poll_desc']}"

        if "graffiti_post" in path:
            for _ in ['db_name','wall','name','text','graffiti_url']:
                inputs[_] = request.form.get(_)
            GraffitiPost(inputs['db_name'], inputs['wall'], inputs['name'], inputs['text'])
            redirect_url = f"{inputs['graffiti_url']}?wall={inputs['wall']}"

        return redirect(redirect_url)

    except:
        return format(traceback.format_exc()), 500,  {'Content-Type': "text/plain"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
