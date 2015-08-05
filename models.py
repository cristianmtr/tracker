from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

## load config secrets
import json
with open('config.json') as config_file:
    config = json.load(config_file)
    
engine = create_engine('mysql+mysqlconnector://{}:{}@localhost:3306/taskfreak'.format(config['username'],config['password']))

Base = automap_base()
# declare objects
Base.prepare(engine, reflect=True)

def create_session():
    session = Session(engine)
    return session

def create_task_object():
    return Base.classes.frk_item

def create_user_object():
    return Base.classes.frk_member
    
def create_tasklist_object():
    return Base.classes.frk_project

def create_comment_object():
    return Base.classes.frk_itemComment
