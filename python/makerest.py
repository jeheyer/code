#!/usr/bin/env python3

def main(request):

    modules = [ "mortgage", "geoip", "get_table" ]

    for _ in modules:

        if "mortgage" in request['path']:
            from financial import GetPaymentData
            return GetPaymentData(**request['query_string'])

        if "geoip" in request['path']:
            from geoip import GeoIP
            from ip_utils import GetClientIP
            ipv4_address = request['path'].split("/")[2]
            if not ipv4_address:
                ipv4_address = GetClientIP()
            return vars(GeoIP(ipv4_address))

        if "getdnsservers" in request['path']:
            from system_tools import GetDNSServersFromToken
            token = request['path'].split("/")[2]
            if not token:
                 token = "testing1234"
            return GetDNSServersFromToken(token)

        if "get_table" in request['path']:
            data = []
            params = request['query_string']
            if 'database' in params and 'table' in params:
                db_name = params['database']
                db_table = params['table']
                if 'join_table' in params:
                    db_join_table = params['join_table']
  
                data.append({db_name: db_table})
            else:
                raise Exception("Must provide database name and table name as arguments")

            from system_tools import GetConfig
            config = GetConfig('mysql')

            from database import MySQLDatabase
            mysql_database = MySQLDatabase(
                config[db_name]['hostname'],
                config[db_name]['username'],
                config[db_name]['password'],
                db_name
            )
            mysql_database.OpenConnection()
            if db_table == "polls":
                rows = mysql_database.SQLQuery("SELECT * FROM polls,{} WHERE polls.poll_name = '{}' AND id = polls.choice_id".format(db_join_table, db_join_table))
            else:
                rows = mysql_database.GetTable(db_table,"ORDER BY id")
            mysql_database.CloseConnection()

            return rows

    return dict(available_modules = modules)

