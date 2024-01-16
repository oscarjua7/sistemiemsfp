from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine =  create_engine ('sqlite:///IEMSFP.db')
db_session = scoped_session(sessionmaker(bind=engine))

Database = declarative_base()