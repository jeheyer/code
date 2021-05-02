#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main(db_name, poll_name, choice_id = 0):

    import sys
    sys.path.insert(1, '../lib/')

    from system_tools import GetConfig
    db_info = GetConfig('mysql', db_name)
    db_info['database'] = db_name

    from database import MySQLDatabase
    mysql_database = MySQLDatabase(db_info)
    mysql_database.OpenConnection()
    table_name = "polls"

    sql_query = f"SELECT num_votes FROM {table_name} WHERE poll_name = '{poll_name}' AND choice_id = {choice_id}"
    result = mysql_database.SQLQuery(sql_query)
    if result:
        num_votes = result[0]['num_votes'] + 1
        sql_update = f"UPDATE {table_name} SET poll_name = '{poll_name}', choice_id={choice_id}, num_votes={num_votes} WHERE poll_name='{poll_name}' AND choice_id={choice_id}"
        mysql_database.SQLQuery(sql_update)
    else:
        sql_insert = f"INSERT INTO {table_name} VALUES ('{poll_name}', {choice_id}, 1)"
        mysql_database.SQLQuery(sql_insert)
    mysql_database.CloseConnection()

if __name__ == '__main__':

    import sys, os, cgi, time, traceback

    sys.stderr = sys.stdout

    try:

        form = cgi.FieldStorage()
        poll_db = form['poll_db'].value
        poll_name = form['poll_name'].value
        poll_desc = form['poll_desc'].value
        poll_url = form['poll_url'].value
        cookie_name = poll_db + "-" + poll_name
        cookie_options = None

        if os.environ.get('REQUEST_METHOD', 'GET') == 'POST':
            cookie_string = os.environ.get('HTTP_COOKIE', None)
            if cookie_string and not cookie_name in cookie_string:
                choice_id = int(form['choice_id'].value)
                if choice_id != 0:
                    main(poll_db, poll_name, choice_id) 
                    cookie_options = "Max-Age=3600;SameSite=Strict;Secure"

        print("Status: 302")
        if cookie_options:
            print(f"Set-Cookie: {cookie_name}=1;{cookie_options}")
        print(f"Location: {poll_url}?poll_name={poll_name}&poll_desc={poll_desc}\n")

    except Exception as e:
        print("Status: 500\nContent-Type: text/plain; charset=UTF-8\n")
        traceback.print_exc(file=sys.stdout, limit=3)

