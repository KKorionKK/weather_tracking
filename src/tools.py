import uuid
import datetime


def get_uuid() -> str:
    return uuid.uuid4().hex


def get_dt() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
