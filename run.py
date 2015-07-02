__author__ = 'CristianMitroi'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

from models import session, Task, User

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'


class TaskAdmin(sqla.ModelView):
    column_exclude_list = [
        'projectId',
        'itemParentId',
        'context',
        'expectedDuration',
        'showInCalendar'
    ]
    #
    column_sortable_list = (
        'description',
        ('responsible','User.username'),
        'deadlineDate'
    )
    #
    form_args = dict(
        description=dict(label="Description", validators=[validators.required()])
    )
    # #
    # # form_ajax_refs = {
    # #     ''
    # # }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(TaskAdmin, self).__init__(Task, session)


class UserAdmin(sqla.ModelView):
    def __init__(self, session):
        super(UserAdmin, self).__init__(User, session)


admin = admin.Admin(app, name='taskfreak improved', template_mode='bootstrap3')

admin.add_view(TaskAdmin(session))
admin.add_view(UserAdmin(session))

if __name__ == '__main__':
    # Start app
    app.run(debug=True, port=5001)
