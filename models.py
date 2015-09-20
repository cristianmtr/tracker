from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(1000), nullable=False)
    responsible = Column(Integer, ForeignKey('user.id'))
    author = Column(Integer, ForeignKey('user.id'))

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)

# load config secrets
import json
with open('config.json') as config_file:
    config = json.load(config_file)

engine = create_engine('mysql+mysqlconnector://{}:{}@localhost:3306/tracker'.format(config['username'],config['password']))
session = Session(engine)

def test_connection:
    try:
        session.query(User).one()
    except Exception as e:
        print "Exception testing db : %s" %str(e)
        # create db
        # create tables