#!/usr/bin/env python3

def main(db_name, wall_name, name, text):

    # Get database configuration info
    from system_tools import GetConfig
    db_info = GetConfig('mysql', db_name)
    db_info['database'] = db_name

    # Do database call
    from database import MySQLDatabase
    mysql_database = MySQLDatabase(db_info)
    mysql_database.OpenConnection()
    table_name = "graffiti"
    sql_insert = f"INSERT INTO {table_name} (`wall_name`,`name`,`text`) VALUES ('{wall_name}','{name}','{text}');"
    mysql_database.SQLQuery(sql_insert)
    mysql_database.CloseConnection()

if __name__ == '__main__':

    import sys, os, cgi, time, traceback

    sys.stderr = sys.stdout

    try:

        if os.environ.get('REQUEST_METHOD', 'GET') == 'POST':
            form = cgi.FieldStorage()
            wall_name = form['wall_name'].value
        else:
            form = {'wall_name': "Test"}
            board_name = form['wall_name']

        if 'name' in form:
            name = form['name'].value
        else:
            name = "Anonymous Coward"
        if 'text' in form:
            text = form['text'].value
        else:
           text = "I have nothing to say"
  
        cookie_name = "graffiti-" + wall_name
        cookie_options = None

        main("primus", wall_name, name, text) 

        if os.environ.get('REQUEST_METHOD', 'GET') == 'POST':
            #if cookie_string and not cookie_name in cookie_string:
            cookie_string = os.environ.get('HTTP_COOKIE', None)
        cookie_options = "Max-Age=300;SameSite=Strict;Secure"

        print("Status: 302")
        if cookie_options:
            print(f"Set-Cookie: {cookie_name}=1;{cookie_options}")
        print(f"Location: https://www.bastardboat.com/graffiti.html?wall_name={wall_name}\n")

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)

