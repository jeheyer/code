#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main(request):

    #import sys
    #sys.path.insert(1, '../lib/')

    modules = [ "mortgage", "geoip", "get_table", "squidread", "getdnsservers", "test"]

    if "test" in request['path']:
        return(request)

    if "mortgage" in request['path']:
        from lib.financial import GetPaymentData
        return GetPaymentData(**request['query_string'])

    if "squidread" in request['path']:
        from squidread import GetSquidData
        data = []
        for host in ["gcp-prox01-p002", "gcp-prox01-p004", "gcp-prox01-p004"]:
            data.extend(GetSquidData(host))
        return data

    if "geoip" in request['path']:
        from lib.geoip import GeoIPList
        geoips = []
        if '/' in request['path'][1:] and not request['path'][-1] == '/':
            ip_list = request['path'].replace("/geoip/", "").split('/')
        else:
            ip_list = [request['client_ip']]
        return GeoIPList(ip_list).geoips

    if "getdnsservers" in request['path']:
        from lib.system_tools import GetDNSServersFromToken
        token = request['path'].split("/")[2]
        if not token:
             token = "testing1234"
        return GetDNSServersFromToken(token)

    if "get_table" in request['path']:
        params = request['query_string']
        if 'database' in params and 'table' in params:
            db_name = params['database']
            db_table = params['table']
            if 'join_table' in params:
                db_join_table = params['join_table']
        else:
            raise Exception("Must provide database name and table name as arguments")

        from lib.system_tools import GetConfig
        db_info = GetConfig('mysql', db_name)
        db_info['database'] = db_name
        from lib.database import MySQLDatabase
        mysql_database = MySQLDatabase(db_info)
        mysql_database.OpenConnection()
        if db_table == "polls":
            sql_query = f"SELECT * FROM polls,{db_join_table} WHERE polls.poll_name = '{db_join_table}' AND id = polls.choice_id"
            rows = mysql_database.SQLQuery(sql_query)
        elif db_table == "graffiti":
            sql_query = f"SELECT * FROM graffiti WHERE wall = '{params['wall']}' ORDER BY timestamp DESC"
            rows = mysql_database.SQLQuery(sql_query)
        else:
            rows = mysql_database.GetTable(db_table)
        mysql_database.CloseConnection()
        return rows

    return dict(available_modules = modules)

# CGI Entry Point
def ParseCGI():
 
    import os, cgi

    request = vars(http_request(os.environ))

    query_fields_objects = cgi.FieldStorage()

    for key in query_fields_objects:
        value = query_fields_objects[key].value
        request['query_string'][key] = str(value)

    return request

# Called via CLI
def ParseCLI():

    import sys

    request = dict(host = "localhost", path = "/", query_string = {}, client_ip = "127.0.0.1")

    # Use argument, if provided, to simulate HTTP Path and query string
    if len(sys.argv) > 1:
       request['path'] = sys.argv[1]
       if '?' in request['path']:
            request['path'], query_string = request['path'].split('?')
            for _ in query_string.split('&'):
                [key, value] = _.split('=')
                request['query_string'][key] = value

    return request

# Old School CGI Entry Point
if __name__ == '__main__':

    import sys, os, json, traceback

    sys.stderr = sys.stdout

    try:
        if 'REQUEST_METHOD' in os.environ:
            request = ParseCGI()
        else:
            request = ParseCLI()

        json_data = json.dumps(main(request), indent=2, default=str)

        print("Content-Length: {}".format(len(json_data)+1))
        print("Cache-Control: no-cache, no-store")
        print("Pragma: no-cache")
        print("Content-Type: application/json; charset=UTF-8\n")
        print(json_data)

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)
