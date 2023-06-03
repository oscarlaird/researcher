from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pathlib import Path
import logging
db_path = Path('./sources.sqlite')
assert db_path.exists()

import os

import prettytable

# Define a base class using SQLAlchemy's `declarative_base`
# This base class will contain metadata about all of our models
Base = declarative_base()


# Define the Source class. This will represent the 'sources' table in our database.
class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    type = Column(String)
    title = Column(String)
    date = Column(Date)
    summary = Column(String)
    entities = Column(String)
    processed = Column(Boolean, default=False)

# create an engine which will interact with the db
# engine = create_engine('sqlite:///sources.sqlite', echo=True)
engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session = sessionmaker(bind=engine)
# If the tables don't exist, this will create them. If they already exist, nothing happens.
Base.metadata.create_all(engine)
# Define a sessionmaker. This will allow us to create new sessions which can interact with the database

import os
from prettytable import PrettyTable
from math import floor

def display_sources():
    with Session() as session:
        sources = session.query(Source).all()
        table = prettytable.PrettyTable()
        table.field_names = ["ID", "URL", "Type", "Title", "Date", "Summary", "Entities", "Processed"]

        # Populate the table with data
        for src in sources:
            table.add_row([getattr(src, field.lower()) for field in table.field_names])

        table.max_width = 50
        table.hrules = prettytable.ALL

        print(table)

def add_source_from_url(url):
    """Add a source to the database from a url"""
    logging.info(f'Adding source for url: {url}')
    with Session() as session:
        # check if a source with this url already exists
        if session.query(Source).filter_by(url=url).first():
            logging.error(f'A source with the url {url} already exists in the database')
        else:
            session.add(Source(url=url))
        session.commit()
