#! /usr/bin/python
from flask import Flask, render_template, jsonify
from models import create_session, create_task_object, create_user_object
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


class Globals(object):
    """Will store db globals"""

    def __init__(self):
        self.session = create_session()
        self.task = create_task_object()
        self.user = create_user_object()
        self.user_id_to_name = {}
        self.build_user_id_to_name()

    def build_user_id_to_name(self):
        users = self.session.query(self.user, self.user.memberId, self.user.firstName).all()
        for u in users:
            self.user_id_to_name[u.memberId] = u.firstName


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/json/<taskid>")
def jsontask(taskid):
    data = [
        'the title',
        'this is the description'.encode('utf-8'),
        '2015-10-22',
        'responsible',
        'author',
        ]
    return jsonify(data=data)

@app.route("/json/")
def json():
    data = []
    tasks = db.session.query(db.task, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId).all()
    for t in tasks:
        this_task = []
        this_task.append(t.title)
        # keep formatting when displaying description
        this_task.append('<div id="{}" data-toggle="modal" data-target="#createNewModal" onclick="updateCurrentItemId(this);"><pre>{}</pre></div>'.format(t.itemId, t.description.encode('utf-8')))
        # handle empty fields, for deadlineDate or member info
        this_task.append(t.deadlineDate.isoformat() if t.deadlineDate else None)
        this_task.append(db.user_id_to_name[t.memberId] if t.memberId != 0 else None)
        this_task.append(db.user_id_to_name[t.authorId] if t.authorId != 0 else None)
        data.append(this_task)
        # data = [
        # ['<a id="edit1" data-toggle="modal" data-target="#createNewModal" data-target="#createNewModal">1</a>', "this is description", "2more", "responsible", "authorId"],
        # ['<button onclick="btnclick(this);">2</button>',"this is description nr 2", "2more", "responsible2", "authorId"],
    # ]
    dataSources = {
        'priority':{
            1: 'Urgent',
            2: 'Medium',
            3: 'Low',
        },
        'tasklist':{
            1: 'Ops',
            2: 'Builds',
            3: 'Whoknows',
        },
        'deadline':{
            1: 'Dummy',
            2: 'Fake',
            3: 'Foo',
            4: 'Bar',
        },
        'responsible':{
            1: 'Cristian',
            2: 'Someone else',
        },
    }
    return jsonify(
        data=data,
        dataSources=dataSources
    )


if __name__ == "__main__":
    app.debug = True
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    db = Globals()
    app.run(host='0.0.0.0', port=80)
