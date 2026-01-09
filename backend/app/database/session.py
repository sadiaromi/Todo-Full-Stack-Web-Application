from sqlmodel import Session, create_engine
from contextlib import contextmanager
from typing import Generator

from .config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug_mode,  # Set to True to see SQL queries in development
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()