import os

from sqlalchemy import Integer, String, Column, ForeignKey, Date, create_engine, Text
from sqlalchemy.orm import declarative_base, Session
from config_data.config import load_config

abspath = os.path.abspath('.env')
config = load_config(abspath)
db_url = config.data_base.token

engine = create_engine(db_url, future=True)


def connect():
    session = Session(bind=engine.connect())
    return session


Base = declarative_base()


class Document(Base):
    __tablename__ = 'Documents'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    psth = Column(String(100), nullable=False)
    date = Column(Date(), nullable=False)


class DocumentText(Base):
    __tablename__ = 'Documents_text'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    id_doc = Column(Integer(), ForeignKey('Documents.id'))
    text = Column(Text(), nullable=False)
