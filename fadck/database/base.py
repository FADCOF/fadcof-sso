# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_NAME, DB_LABEL

engine_url = {
    'sqlite3': 'sqlite:///storage/{}/databases/{}.sqlite3'
}


def db_url(url_type: str, server_name: str, service_name: str) -> str:
    if url_type not in engine_url:
        raise NotImplementedError('Not support database "{}"'.format(url_type))
    return engine_url[url_type].format(server_name, service_name)


main_engine = create_engine(db_url(DB_NAME, 'main', DB_LABEL), connect_args={"check_same_thread": False})
backup_engine = create_engine(db_url(DB_NAME, 'backup', DB_LABEL), connect_args={"check_same_thread": False})

MainSession = sessionmaker(autoflush=False, bind=main_engine)
BackupSession = sessionmaker(autoflush=False, bind=backup_engine)

Base = declarative_base()


def get_session():
    from fadck.storage import dir
    if dir.MAIN_POOL_VALID:
        return MainSession()
    if dir.BACKUP_POOL_VALID:
        return BackupSession()
    raise RuntimeError('No database is valid.')


def startup():
    # Make the database directory.
    from fadck.storage.dir import ensure as ensure_dir
    ensure_dir('databases')
    # Build all the necessary tables.
    Base.metadata.create_all(bind=main_engine)
    Base.metadata.create_all(bind=backup_engine)
