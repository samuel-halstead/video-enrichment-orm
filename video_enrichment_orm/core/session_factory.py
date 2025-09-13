from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from video_enrichment_orm.core.config import settings
from video_enrichment_orm.exceptions.integrity_exception import IntegrityExceptionError
from video_enrichment_orm.exceptions.internal_server_error import (
    InternalServerExceptionError,
)


class DatabaseSessionManager:
    _engine = None
    _SessionFactory = None

    @classmethod
    def initialize(cls):
        """Initialize the database engine and session factory once."""
        if cls._engine is None or cls._SessionFactory is None:
            cls._engine = create_engine(
                settings.POSTGRES_CONNECTION_URL,
                pool_pre_ping=True,
                connect_args={"application_name": settings.POSTGRES_APP_NAME},
            )
            cls._SessionFactory = scoped_session(sessionmaker(bind=cls._engine, expire_on_commit=False))

    @classmethod
    def get_session_factory(cls) -> scoped_session:
        """Return the singleton session factory."""
        if cls._SessionFactory is None:
            cls.initialize()
        return cls._SessionFactory

    @classmethod
    def dispose(cls):
        """Dispose the engine and reset the session factory (for cleanup or testing)."""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._SessionFactory = None


# Use this context manager for scoped sessions
@contextmanager
def session_scope() -> Session:
    session_factory = DatabaseSessionManager.get_session_factory()
    session = session_factory()
    try:
        yield session
        session.commit()
    except IntegrityExceptionError as error:
        session.rollback()
        raise IntegrityExceptionError(error) from error
    except InternalServerExceptionError as error:
        session.rollback()
        raise InternalServerExceptionError(error) from error
    except ValueError as error:
        session.rollback()
        raise ValueError(str(error)) from error
    except Exception as error:
        session.rollback()
        raise Exception(str(error)) from error
    finally:
        session_factory.remove()
