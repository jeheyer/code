def GraffitiPost(db_name: str, wall: str, name: str = "Anonymous Coward", text: str = "I have nothing to say", client_ip = None) -> bool:

    # Get database configuration info
    from lib.system_tools import GetConfig
    db_info = GetConfig('mysql', db_name)
    db_info['database'] = db_name

    # Do database call
    from lib.database import MySQLDatabase
    mysql_database = MySQLDatabase(db_info)
    mysql_database.OpenConnection()
    table_name = "graffiti"
    if client_ip:
        sql_insert = f"INSERT INTO {table_name} (`wall`,`name`,`text`,`client_ip`) VALUES ('{wall}','{name}','{text}','{client_ip}');"
    else:
        sql_insert = f"INSERT INTO {table_name} (`wall`,`name`,`text`) VALUES ('{wall}','{name}','{text}');"
    mysql_database.SQLQuery(sql_insert)
    mysql_database.CloseConnection()

def PollVote(db_name: str, poll_name: str, choice_id: int = 0) -> bool:

    # Retrieve database configuration
    from lib.system_tools import GetConfig
    db_info = GetConfig('mysql', db_name)
    db_info['database'] = db_name

    # Connect to Database
    from lib.database import MySQLDatabase
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
