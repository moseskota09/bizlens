from sqlalchemy.orm import Session

from app.core.database import get_db


def get_db_session() -> Session:
    yield from get_db()
