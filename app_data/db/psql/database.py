import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app_data.db.psql.models import Base

load_dotenv(verbose=True)

database_url = os.environ['POSTGRES_URL']
engine = create_engine(database_url)

_session_maker = sessionmaker(bind=engine)

def create_db():
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
    except Exception as e:
        print(str(e))

def create_tables():
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        print(str(e))

def session_maker():
    return _session_maker()


if __name__ == '__main__':
    create_db()
    create_tables()