#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def application(environ, start_response):

    import traceback

    try:

        x = "https://www.bastardboat.com/pollresults.html"
        start_response(301, 'Location: ' + x)
        return [ ]

    except:

        start_response('500 Internal Server Error', response_headers)
        return [ str(traceback.format_exc()).encode('utf-8') ]

