#!/usr/bin/env python3

def main(request):

    modules = [ "mortgage", "geoip", "get_table" ]

    for _ in modules:

        if "mortgage" in request['path']:
            from financial import GetPaymentData
            return GetPaymentData(**request['query_string'])

        if "geoip" in request['path']:
            from geoip import GeoIP
            ipv4_address = request['path'].split("/")[2]
            if not ipv4_address:
                ipv4_address = request['client_ip']
            return vars(GeoIP(ipv4_address))

        if "getdnsservers" in request['path']:
            from system_tools import GetDNSServersFromToken
            token = request['path'].split("/")[2]
            if not token:
                 token = "testing1234"
            return GetDNSServersFromToken(token)

        if "get_table" in request['path']:

            if 'database' in params and 'table' in request['query_string']:
                db_name = request['query_string']['database']
                db_table = request['query_string']['table']
                if 'join_table' in request['query_string']:
                    db_join_table = request['query_string']['join_table']
  
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
            else:
                rows = mysql_database.GetTable(db_table,"ORDER BY id")
            mysql_database.CloseConnection()

            return rows

    return dict(available_modules = modules)

