#!/usr/bin/env python3

from traceback import format_exc


def get_client_ip(headers={}):

    try:
        # Convert all keys to lower case for consistency
        _ = {k.lower(): v for k, v in headers.items()}
        x_appengine_user_ip = _.get('http_x_appengine_user_ip')
        x_real_ip = _.get('http_x_real_ip')
        x_forwarded_for = _.get('http_x_forwarded_for')
        remote_addr = _.get('remote_addr', "127.0.0.1")

        if x_appengine_user_ip:
            return x_appengine_user_ip
        if x_real_ip:
            return x_real_ip
        if x_forwarded_for:
            if ", " in x_forwarded_for:
                return x_forwarded_for.split(", ")[-2]
            return x_forwarded_for
        return remote_addr

    except Exception as e:
        raise Exception(format_exc())


def ping(headers={}, request=None) -> dict:

    from platform import node, system, release, machine, processor
    from socket import gethostbyname
    from sys import version

    info = {}

    header_names = ('HTTP_HOST', 'SERVER_NAME', 'SERVER_ADDR', 'SERVER_SOFTWARE', 'SERVER_PROTOCOL', 'SERVER_PORT',
        'REMOTE_ADDR', 'HTTP_X_REAL_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED_PROTO', 'HTTP_CONNECTION',
        'PATH_INFO', 'REQUEST_URI', 'RAW_URI', 'SCRIPT_NAME', 'QUERY_STRING', 'HTTP_USER_AGENT', 'REQUEST_METHOD'
    )

    try:

        # Standard environment variables in dictionary
        if isinstance(headers, dict):
            for header_name in header_names:
                header_name = header_name.lower()
                info[header_name] = headers.get(header_name.upper())
            if not 'request_uri' in info:
                 info['request_uri'] = headers.get('RAW_URI')
            if not 'raw_uri' in info:
                 info['raw_uri'] = headers.get('REQUEST_URI')

        # Request object
        if request:
            for header_name in header_names:
                try:
                    header_name = header_name.lower()
                    info[header_name] = str(getattr(request, header_name))
                except AttributeError:
                    info[header_name] = None
                else:
                    continue

            info['server_name'] = node()
            info['server_addr'] = gethostbyname(info['server_name'])
            info['http_user_agent'] = request.headers.get("User-Agent")
            info['http_connection'] = request.headers.get('Connection')

            if 'quart' in str(request.__class__):
                info['http_host'] = request.host.split(':')[0]
                info['path_info'] = request.path
                info['server_port'] = int(request.server[1])
                info['server_protocol'] = "HTTP/" + request.http_version
                info['remote_addr'] = request.remote_addr
                info['headers'] = str(request.headers)
                info['server_protocol'] = "HTTP/" + request.http_version
                info['http_x_real_ip'] = request.headers.get('X-Real-IP')
                info['http_x_forwarded_for'] = request.headers.get('X-Forwarded-For')
                info['http_x_forwarded_proto'] = request.headers.get('X-Forwarded-Proto')
                #info['headers'] = str(request.headers)

            if 'starlette' in str(request.__class__):
                info['http_host'] = request.headers['host'].split(':')[0]
                info['path_info'] = request.url.path
                info['server_port'] = int(request.get('server', [])[1])
                #info['remote_addr'] = request['client'][0]
                info['remote_addr'] = request.client.host
                info['headers'] = str(request.headers)
                info['server_protocol'] = "HTTP/" + request.get('http_version')
                info['request_method'] = request.method
                info['http_x_real_ip'] = request.headers.get('x-real-ip')
                info['http_x_forwarded_for'] = request.headers.get('x-forwarded-for')
                info['http_x_forwarded_proto'] = request.headers.get('x-forwarded-proto')
                #info['headers'] = request.headers

            info['script_name'] = info['path_info']

        info['client_ip'] = get_client_ip(info)
        info['platform_node'] = node()
        info['platform_os'] = "{} {}".format(system(), release())
        info['platform_cpu'] = "{}/{}".format(machine(), processor())
        info['python_info'] = str(version).split()[0]
        #info['environ'] = str(environ)

        return info

    except Exception as e:
        raise Exception(format_exc())


def mortgage(options={}):

    from financial import GetPaymentData

    try:
        return GetPaymentData(options)
    except Exception as e:
        raise Exception(format_exc())


async def graffiti(db_name, wall):

    from database import db_engine, db_engine_dispose, db_get_table

    try:
        engine = await db_engine(db_name)
        posts = await db_get_table(engine, "graffiti", where={'wall': wall})
        await db_engine_dispose(engine)
        return posts
    except Exception as e:
        raise Exception(format_exc())


async def polls(db_name, db_join_table):

    from database import db_engine, db_engine_dispose, db_get_table

    try:
        engine = await db_engine(db_name)
        results = await db_get_table(engine, "polls", join_table_name=db_join_table)
        await db_engine_dispose(engine)
        return results
    except Exception as e:
        raise Exception(format_exc())


async def get_table(db_name, db_table=None, db_join_table=None, wall=None):

    from database import db_engine, db_engine_dispose, db_get_table

    try:
        engine = await db_engine(db_name)
        results = await db_get_table(engine, db_table)
        await db_engine_dispose(engine)
        return results
    except Exception as e:
        raise Exception(format_exc())


    """
        if db_table == "polls":
            result = await get_table(engine, db_table, db_join_table, {'wall': wall, 'name': name, 'text': text})
        if db_table == "graffiti":
            result = await get_table(engine, db_table, where={'wall': wall})
        await db_engine_dispose(engine)

        async with engine.begin() as conn:
            table = await conn.run_sync(lambda conn: Table(db_table, MetaData(), autoload_with=conn))
            column_names = [c.name for c in table.columns]
            if db_join_table:
                join_table = await conn.run_sync(lambda conn: Table(db_join_table, MetaData(), autoload_with=conn))
                column_names.extend([c.name for c in join_table.columns])

        if db_table == "polls":
            async with AsyncSession(engine) as session:
                statement = select(table, join_table)\
                    .filter(table.columns.poll_name == db_join_table)\
                    .filter(join_table.columns.id == table.columns.choice_id)\
                    .order_by(table.columns.num_votes.desc())
                result = await session.execute(statement)
            await db_engine_dispose(engine, session)
        else:
            async with engine.connect() as conn:
                if db_table == "graffiti":
                    statement = table.select().where(table.columns.wall == wall).order_by(table.columns.timestamp.desc())
                    result = await conn.execute(statement)
                else:
                    result = await conn.execute(select(table))
            await db_engine_dispose(engine)

        # Convert to dictionary with the column name as key
        rows = []
        for row in result:
            rows.append(dict(zip(column_names, row)))

        return rows

    except:
        raise Exception(format_exc())
"""


async def graffiti_post(db_name, wall, graffiti_url=None, name=None, text=None):

    from database import db_engine, db_engine_dispose, db_insert

    if not graffiti_url:
        graffiti_url = "http://localhost"
    if not name:
        name = "Anonymous Coward"
    if not text:
        text = "I have nothing to say"

    try:
        engine = await db_engine(db_name)
        result = await db_insert(engine, "graffiti", {'wall': wall, 'name': name, 'text': text})
        await db_engine_dispose(engine)
        return f"{graffiti_url}?wall={wall}"
    except Exception as e:
        raise Exception(format_exc())


async def poll_vote(db_name: str, poll_name: str, poll_url: str, poll_desc: str, choice_id: int):

    from database import db_engine, db_engine_dispose, db_get_table, db_insert, db_update

    if not poll_url:
        poll_url = "http://localhost"

    poll_url = f"{poll_url}?poll_name={poll_name}&poll_desc={poll_desc}"

    choice_id = int(choice_id)
    if choice_id < 1:
        return poll_url

    try:

        engine = await db_engine(db_name)

        results = await db_get_table(engine, "polls", join_table_name=poll_name)
        if len(results) > 0:
            return results
            result = await db_update(engine, "polls", {'poll_name': poll_name, 'choice_id': choice_id, 'num_votes': 1})
        else:
            result = await db_insert(engine, "polls", {'poll_name': poll_name, 'choice_id': choice_id, 'num_votes': 1})
        """
        session = orm.sessionmaker(bind=engine)()

        table = Table("polls", MetaData(), autoload_with=engine)

        # See if this choice has existing votes
        result = session.query(table.columns.num_votes)\
            .filter(table.columns.poll_name == poll_name)\
            .filter(table.columns.choice_id == choice_id)\
            .all()
        if len(result) > 0:
            num_votes = result[0][0] + 1
            statement = table.update()\
                .filter(table.columns.poll_name == poll_name)\
                .filter(table.columns.choice_id == choice_id)\
                .values(num_votes=num_votes)
        else:
            statement = table.insert().values(poll_name=poll_name, choice_id=choice_id, num_votes=1)

        result = session.execute(statement)
        """

        await db_engine_dispose(engine)

        return poll_url

    except Exception as e:
        raise Exception(format_exc())


def get_geoip_info(geoiplist=["127.0.0.1"]):

    from geoip import GeoIPList

    try:
        return GeoIPList(geoiplist).geoips
    except Exception as e:
        raise Exception(format_exc())


def get_dns_servers(token="testing1234"):

    from system_tools import GetDNSServersFromToken

    try:
        return GetDNSServersFromToken(token)
    except Exception as e:
        raise Exception(format_exc())


if __name__ == '__main__':

    from os import environ
    from pprint import pprint

    pprint(ping(environ))
