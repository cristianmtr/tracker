from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import json


def create_engine_from_config(config_file="config.json"):
    with open(config_file) as config_file_handle:
        config = json.load(config_file_handle)
        print "Using config:"
        print json.dumps(config, sort_keys=False, indent=4, separators=(',',': '))
    engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' %(config['username'],config['password'], config['host'], config['port'], config['database']))
    return engine



# declare objects
class Globals(object):
    """Will store db globals"""

    def __init__(self):
        Base = automap_base()
        engine = create_engine_from_config()
        Base.prepare(engine, reflect=True)
        self.session = Session(engine)
        self.task = Base.classes.frk_item
        self.user = Base.classes.frk_member
        self.tasklist = Base.classes.frk_project
        self.comment = Base.classes.frk_itemComment
        self.history = Base.classes.frk_itemStatus


    def try_flush_session(self):
        """tries to flush session
    if it fails, it rolls back and returns -1
    it it's ok, return 0"""
        try:
            self.session.flush()
            return 0
        except Exception as e:
            print 'ERROR FLUSHING DB: {}\nROLLING BACK'.format(e)
            self.session.rollback()
            return -1

# db = Globals()
