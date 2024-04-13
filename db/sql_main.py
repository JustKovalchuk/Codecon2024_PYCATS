from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


BaseModel = declarative_base()
db_connection = None
Session = None
session = None
engine = None


def get_con():
    return db_connection


def get_session():
    return session


def set_con(con):
    global db_connection
    db_connection = con


def create_connection(hostname, username, password, database_name):
    global engine, Session, session
    try:
        str = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{database_name}"
        if not database_exists(str):
            create_database(str)
        engine = create_engine(str)
        BaseModel.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        session.commit()

        print("Connected db successfully!")
        return engine.connect()
    except Exception as e:
        print(e)
        return None