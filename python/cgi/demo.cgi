#!/usr/bin/env python3

if __name__ == "__main__":

    import os, cgi

    server_host = os.environ.get('HTTP_HOST', 'localhost')
    server_port = os.environ.get('SERVER_PORT', 80)
    path = os.environ.get('SCRIPT_URL', '/')
    query_params = {}
    _ = cgi.FieldStorage()
    for key in _:
        query_params[key] = str(_[key].value)
    print("Content-type: text\plain\n\n")
    print(query_params)
