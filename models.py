from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
import json
import sys


def create_engine_from_config(config_file="config.json"):
    with open(config_file) as config_file_handle:
        config = json.load(config_file_handle)
        print "Using config:"
        print json.dumps(config, sort_keys=False, indent=4, separators=(',', ': '))
    engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' % (
    config['username'], config['password'], config['host'], config['port'], config['database']))
    return engine


# declare objects
class Globals(object):
    """Will store db globals"""

    def __init__(self):
        Base = automap_base()
        engine = create_engine_from_config()
        Base.prepare(engine, reflect=True)
        self.session = sessionmaker()
        self.session.configure(bind=engine)
        self.task = Base.classes.frk_item
        self.user = Base.classes.frk_member
        self.tasklist = Base.classes.frk_project
        self.comment = Base.classes.frk_itemComment
        self.history = Base.classes.frk_itemStatus

    def try_commit(self, session):
        """
        tries to commit session as is
        :rtype : int
        returns 0 on success
        - 1 on fail
        """
        try:
            session.commit()
            return 0
        except Exception as e:
            print >> sys.stderr, 'ERROR COMMITTING DB: {}\nROLLING BACK'.format(e)
            session.rollback()
            return -1
