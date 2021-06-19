#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from paste import request
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
            if int(inputs['choice_id']) > 0:
                PollVote(inputs['poll_db'], inputs['poll_name'], inputs['choice_id'])
            redirect_url = f"{inputs['poll_url']}?poll_name={inputs['poll_name']}&poll_desc={inputs['poll_desc']}"

        if "graffiti_post" in path:
            fields = request.parse_formvars(environ)
            for _ in ['db_name','wall','name','text','graffiti_url']:
                inputs[_] = fields.get(_, "")
            if inputs['name'] == "":
                inputs['name'] = "Anonymous Coward"
            if inputs['text'] == "":
                inputs['text'] = "I have nothing to say"
            client_ip = "127.0.0.1"
            GraffitiPost(inputs['db_name'], inputs['wall'], inputs['name'], inputs['text'], client_ip)
            redirect_url = f"{inputs['graffiti_url']}?wall={inputs['wall']}"

        start_response('302 ', [('Location', redirect_url)])
        return []

    except:

        response_headers = [ ('Content-type', 'text/plain') ]
        start_response('500 Internal Server Error', response_headers)
        return [ str(traceback.format_exc()).encode('utf-8') ]
