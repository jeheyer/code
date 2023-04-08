from sqlalchemy import Table, MetaData, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


async def db_engine(db_name):

    from os import path
    from tomli import load

    try:
        # Get Database connection info
        pwd = path.realpath(path.dirname(__file__))
        cfg_file = path.join(pwd, "../../../private/cfg/db_config.toml")
        with open(cfg_file, mode="rb") as fp:
            db_info = load(fp).get(db_name)
            if not db_info:
                raise Exception("Database config not found for '{}'".format(db_name))

        # Connect to DB
        db_hostname = db_info.get('hostname', "127.0.0.1")
        db_username = db_info.get('username', "root")
        db_password = db_info.get('password', "")
        db_type = db_info.get('driver', "mysql").lower()
        if db_type == "mysql":
            db_driver = "mysql+asyncmy"
        engine = create_async_engine("{}://{}:{}@{}/{}".format(db_driver, db_username, db_password, db_hostname, db_name))
        return engine

    except Exception as e:
        raise e


async def db_engine_dispose(engine=None, session=None):

    # Disconnect from DB
    if engine:
        await engine.dispose()
    if session:
        await session.close()


async def db_insert(engine, table_name, values={}):

    try:
        async with engine.begin() as conn:
            table = await conn.run_sync(lambda conn: Table(table_name, MetaData(), autoload_with=conn))
            statement = table.insert().values(values)
            result = await conn.execute(statement)
            return result

    except Exception as e:
        raise e


async def db_get_table(engine, table_name, join_table_name=None, where={}, order_by={}):

    from sqlalchemy import Table, MetaData, select
    from sqlalchemy.ext.asyncio import AsyncSession

    try:

        async with engine.begin() as conn:
            table = await conn.run_sync(lambda conn: Table(table_name, MetaData(), autoload_with=conn))
            column_names = [c.name for c in table.columns]
            #return column_names
            if join_table_name:
                join_table = await conn.run_sync(lambda conn: Table(join_table_name, MetaData(), autoload_with=conn))
                column_names.extend([c.name for c in join_table.columns])

        if join_table_name:
            async with AsyncSession(engine) as session:
                statement = select(table, join_table)\
                    .filter(table.columns.poll_name == join_table_name)\
                    .filter(join_table.columns.id == table.columns.choice_id)\
                    .order_by(table.columns.num_votes.desc())
                result = await session.execute(statement)
        else:
            async with engine.connect() as conn:
                if where:
                    statement = table.select().where(table.columns.wall == where['wall']).order_by(table.columns.timestamp.desc())
                    result = await conn.execute(statement)
                else:
                    result = await conn.execute(select(table))

        # Convert to dictionary with the column name as key
        rows = []
        for row in result:
            rows.append(dict(zip(column_names, row)))

        return rows

    except Exception as e:
        raise e

