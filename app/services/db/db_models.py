import asyncpg

from app.misc.logger import logger
from app.settings.config import load_config


async def create_all_tables(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        await conn.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id varchar(255) PRIMARY KEY,
                    login varchar(255) UNIQUE NOT NULL,
                    password varchar(64) NOT NULL,
                    balance int NOT NULL DEFAULT 10
                )
            ''')

        await conn.execute('''
                CREATE TABLE IF NOT EXISTS tickets(
                    user_id varchar(255) REFERENCES users(id),
                    ticket_id varchar(255) PRIMARY KEY NOT NULL,
                    status varchar(255) NOT NULL,
                    datetime timestamp NOT NULL,
                    messages json NOT NULL
                )
                ''')

        await conn.execute('''
                CREATE TABLE IF NOT EXISTS requests(
                    user_id varchar(255) REFERENCES users(id),
                    request_id varchar(255) PRIMARY KEY NOT NULL,
                    datetime timestamp NOT NULL,
                    source_file_size float NOT NULL,
                    result_file_size float NOT NULL
                )
                ''')

        await conn.execute('''
                CREATE TABLE IF NOT EXISTS payments(
                    user_id varchar(255) REFERENCES users(id),
                    transaction_id varchar(255) PRIMARY KEY NOT NULL,
                    datetime timestamp NOT NULL,
                    credits float NOT NULL,
                    balance_total int NOT NULL
                )
                ''')


async def drop_all_tables(pool):
    async with pool.acquire() as conn:
        await conn.execute("DROP TABLE users CASCADE")
        logger.info("All tables were dropped")


async def create_db() -> asyncpg.Pool:
    logger.info("Connecting to database")

    config = load_config()
    db_config = config.db

    pool = pool = await asyncpg.create_pool(
        user=db_config.user,
        password=db_config.password,
        database=db_config.database,
        host=db_config.host,
    )

    logger.info(f"Created DB Pool with min={pool._minsize} max={pool._maxsize}")

    await create_all_tables(pool)

    return pool
