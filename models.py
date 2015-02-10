from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import time


import sqlalchemy.orm as o

engine = create_engine(
    'mssql+pymssql://sa:kfsql@localhost:1433/test', echo=True)

Base = declarative_base()
metadata = Base.metadata


class entries(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)

    def __repr__(self):
        return "<entries(id='%s' , title='%s')>" % \
            (self.id, self.title)


def init_db():
    metadata.create_all(bind=engine)

DBSession = o.sessionmaker(bind=engine)
s = DBSession()
