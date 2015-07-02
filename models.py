from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, relationship, backref

## load config secrets
import json
with open('config.json') as config_file:
    config = json.load(config_file)
    
engine = create_engine('mysql+mysqlconnector://{}:{}@localhost:3306/taskfreak'.format(config['username'],config['password']))

Base = automap_base()
# declare objects


class Task(Base):
    __tablename__ = 'frk_item'
    responsible = Column("memberId", ForeignKey('frk_member.memberId'))
    author = Column("authorId", ForeignKey('frk_member.memberId'))
    # responsible = relationship(User, backref='tasks_assigned')
    # author = relationship(User, )


class User(Base):
    __tablename__ = 'frk_member'
    username = Column('firstName', String)
    # tasks_assigned = relationship("Task", backref="responsible")
    # tasks_created = relationship("Task", backref="author")

session = Session(engine)
Base.prepare(engine, reflect=True)
