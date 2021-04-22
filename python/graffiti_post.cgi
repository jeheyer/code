#!/usr/bin/env python3

def main(db_name, board_name, name, text):

    from system_tools import GetConfig
    db_info = GetConfig('mysql', db_name)
    db_info['database'] = db_name

    from database import MySQLDatabase
    mysql_database = MySQLDatabase(db_info)
    mysql_database.OpenConnection()
    table_name = "graffiti"

    sql_insert = f"INSERT INTO {table_name} VALUES ('{board_name}', {name}, {text})"
    mysql_database.SQLQuery(sql_insert)
    mysql_database.CloseConnection()

if __name__ == '__main__':

    import sys, os, cgi, time, traceback

    sys.stderr = sys.stdout

    try:

        form = cgi.FieldStorage()
        board_name = form['board_name'].value
        name = form['name'].value
        text = form['text'].value
        cookie_name = "graffiti-" + board_name
        cookie_options = None

        if os.environ.get('REQUEST_METHOD', 'GET') == 'POST':
            cookie_string = os.environ.get('HTTP_COOKIE', None)
            if cookie_string and not cookie_name in cookie_string:
                main("primus", board_name, name, text) 
                cookie_options = "Max-Age=300;SameSite=Strict;Secure"

        print("Status: 302")
        if cookie_options:
            print(f"Set-Cookie: {cookie_name}=1;{cookie_options}")
        print(f"Location: graffiti.html?board_name={board_name}\n")

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)

