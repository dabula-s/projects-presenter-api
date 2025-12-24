from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from infrastructure.db.postgres.base import sync_engine


def get_sync_session():
    with sync_engine.connect() as connection:
        with connection.begin() as transaction:
            _SyncSession = sessionmaker(bind=connection)
            with _SyncSession() as session:
                try:
                    yield session
                    session.commit()
                except:  # noqa:E722
                    transaction.rollback()
                    raise


sync_session_manager = contextmanager(get_sync_session)
