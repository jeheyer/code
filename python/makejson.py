#!/usr/bin/env python3

def GetClientIP(env):

    return "127.0.0.1"

def main(request):

    modules = [ "mortgage", "geoip", "get_table", "squidread"]

    if "mortgage" in request['path']:
        from financial import GetPaymentData
        return GetPaymentData(**request['query_string'])

    if "squidread" in request['path']:
        from squidread import GetSquidData
        data = []
        for host in ["gcp-prox01-p002", "gcp-prox01-p004", "gcp-prox01-p004"]:
            data.extend(GetSquidData(host))
        return data

    if "geoip" in request['path']:
        from geoip import GeoIP
        if '/' in request['path'][1:] and not request['path'][-1] == '/':
            ipv4_address = request['path'].split("/")[2]
        else:
            ipv4_address = request['client_ip']
        return vars(GeoIP(ipv4_address))

    if "getdnsservers" in request['path']:
        from system_tools import GetDNSServersFromToken
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

        from system_tools import GetConfig
        db_info = GetConfig('mysql', db_name)
        db_info['database'] = db_name
        from database import MySQLDatabase
        mysql_database = MySQLDatabase(db_info)
        mysql_database.OpenConnection()
        if db_table == "polls":
            rows = mysql_database.SQLQuery("SELECT * FROM polls,{} WHERE polls.poll_name = '{}' AND id = polls.choice_id".format(db_join_table, db_join_table))
        if db_table == "graffiti":
            rows = mysql_database.SQLQuery("SELECT * FROM graffiti WHERE board_name = '{}'".format(params['board_name']))
        else:
            rows = mysql_database.GetTable(db_table)
        mysql_database.CloseConnection()
        return rows

    return dict(available_modules = modules)
