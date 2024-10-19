import os
from dotenv import dotenv_values


env = dotenv_values(os.getcwd() + "/.env")

PARSE_GAP_SECONDS = 180

PG_NAME = env.get("PG_NAME")
PG_USER = env.get("PG_USER")
PG_PASSWORD = env.get("PG_PASSWORD")
PG_ADAPTER = env.get("PG_ADAPTER")
PG_HOST = env.get("PG_HOST")
PG_PORT = int(env.get("PG_PORT"))
PG_SYNC_ADAPTER = env.get("PG_SYNC_ADAPTER")


def get_connection_string(sync: bool = False) -> str:
    if sync:
        return (
            f"{PG_SYNC_ADAPTER}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"
        )
    return f"{PG_ADAPTER}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_NAME}"
