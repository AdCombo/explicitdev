from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy.orm import Session


@contextmanager
def session_scope(constructed_session) -> ContextManager[Session]:
    """Based on recipe from there https://docs.sqlalchemy.org/en/13/orm/session_basics.html"""
    session = constructed_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


__all__ = [
    session_scope.__name__,
]
