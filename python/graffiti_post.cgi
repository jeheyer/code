#!/usr/bin/env python3

def main(db_name, wall, name, text):

    # Get database configuration info
    from system_tools import GetConfig
    db_info = GetConfig('mysql', db_name)
    db_info['database'] = db_name

    # Do database call
    from database import MySQLDatabase
    mysql_database = MySQLDatabase(db_info)
    mysql_database.OpenConnection()
    table_name = "graffiti"
    sql_insert = f"INSERT INTO {table_name} (`wall`,`name`,`text`) VALUES ('{wall}','{name}','{text}');"
    mysql_database.SQLQuery(sql_insert)
    mysql_database.CloseConnection()

if __name__ == '__main__':

    import sys, os, cgi, time, traceback

    sys.stderr = sys.stdout

    try:

        if os.environ.get('REQUEST_METHOD', 'GET') == 'POST':
            form = cgi.FieldStorage()
            wall = form['wall'].value
        else:
            form = {'wall': "Test"}
            wall = form['wall']

        db_name = form['db_name'].value

        if 'name' in form:
            name = form['name'].value
        else:
            name = "Anonymous Coward"
        if 'text' in form:
            text = form['text'].value
        else:
           text = "I have nothing to say"
  
        cookie_name = "graffiti-" + wall
        cookie_options = None

        main(db_name, wall, name, text) 

        if os.environ.get('REQUEST_METHOD', 'GET') == 'POST':
            #if cookie_string and not cookie_name in cookie_string:
            cookie_string = os.environ.get('HTTP_COOKIE', None)
        cookie_options = "Max-Age=300;SameSite=Strict;Secure"

        print("Status: 302")
        if cookie_options:
            print(f"Set-Cookie: {cookie_name}=1;{cookie_options}")
        print(f"Location: {graffiti_url}?wall={wall}\n")

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)

