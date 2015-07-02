__author__ = 'CristianMitroi'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

from models import create_session, create_task_object, create_user_object

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'

class DbObject(object):
    """Will store db globals"""

    def __init__(self):
        self.session = create_session()
        self.task = create_task_object()
        self.user = create_user_object()

db = DbObject()

class TaskAdmin(sqla.ModelView):
    column_exclude_list = ['Projectid']
    
    def __init__(self, session):
        # Just call parent class with predefined model.
        super(TaskAdmin, self).__init__(db.task, db.session)


class UserAdmin(sqla.ModelView):
    def __init__(self, session):
        super(UserAdmin, self).__init__(db.user, db.session)


admin = admin.Admin(app, name='taskfreak improved', template_mode='bootstrap3')

admin.add_view(TaskAdmin(db.session))
admin.add_view(UserAdmin(db.session))

if __name__ == '__main__':
    # Start app
    app.run(debug=True)
