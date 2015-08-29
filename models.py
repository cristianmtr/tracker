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

class Globals(object):
    """Will store db globals"""

    def __init__(self):
        self.session = create_session()
        self.task = create_task_object()
        self.user = create_user_object()
        self.tasklist = create_tasklist_object()
        self.comment = create_comment_object()
        self.history = create_history_object()


def build_user_id_to_name():
    """returns dictionary mapping users ids to user names"""
    user_id_to_name = {}
    users = db.session.query(db.user, db.user.memberId, db.user.firstName).all()
    for u in users:
        user_id_to_name[u.memberId] = u.firstName
    return user_id_to_name


def build_tasklist_id_to_name():
    """returns dictionary mapping tasklist (projects) IDs to their names"""
    tasklists_dict = {}
    all_tasklists = db.session.query(db.tasklist, db.tasklist.projectId, db.tasklist.name).all()
    for tsklst in all_tasklists:
        tasklists_dict[tsklst.projectId] = tsklst.name
    return tasklists_dict


def build_priority_id_to_name():
    """returns dictionary mapping priority ids to names"""
    priority = {
        1: 'Urgent',
        2: 'High priority',
        3: 'Medium',
        4: 'Normal',
        5: 'Low priority',
        6: 'Low priority',
        7: 'Very Low priority',
        8: 'Very Low priority',
        9: 'Whatever',
    }
    return priority


def tryFlushSession():
    """tries to flush session
if it fails, it rolls back and returns -1
it it's ok, return 0"""
    try:
        db.session.flush()
        return 0
    except Exception as e:
        print 'ERROR FLUSHING DB: {}\nROLLING BACK'.format(e)
        db.session.rollback()
        return -1


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

def create_history_object():
    return Base.classes.frk_itemStatus

db = Globals()