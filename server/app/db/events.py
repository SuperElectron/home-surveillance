
from loguru import logger
from fastapi import FastAPI
from pymongo import MongoClient 

from app.core.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.utils.sync import run_in_thread

async def connect_to_db(app: FastAPI) -> None:
    logger.info(
        """
        Establishing connection to database {0} with user {1} on host and port {2}:{3}
        """,
        repr(DB_NAME),
        repr(DB_USER),
        repr(DB_HOST),
        repr(DB_PORT),
    )

    db_url = "mongodb://{user}:{password}@{host}".format(user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    client = await run_in_thread(MongoClient, db_url, uuidRepresentation="standard")
    database = client[DB_NAME]

    app.state.db = database
    app.state.client = client

    logger.info("Connection established.")

async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database.")

    await run_in_thread(app.state.client["__instance"].client.close)

    logger.info("Connection closed.")