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


@app.route("/json")
def json():
    data = []
    tasks = db.session.query(db.task, db.task.itemId, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId).all()
    for t in tasks:
        this_task = []
        this_task.append(t.itemId)
        # keep formatting when displaying description
        this_task.append("<pre>" + t.description + "</pre>")
        # handle empty fields, for deadlineDate or member info
        this_task.append(t.deadlineDate.isoformat() if t.deadlineDate else None)
        this_task.append(db.user_id_to_name[t.memberId] if t.memberId != 0 else None)
        this_task.append(db.user_id_to_name[t.authorId] if t.authorId != 0 else None)
        data.append(this_task)
    # data = [
    #     [1,"this is description", "2more", "responsible", "authorId"],
    #     [2,"this is description nr 2", "2more", "responsible2", "authorId"],
    # ]
    return jsonify(data=data)


if __name__ == "__main__":
    app.debug = True
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    db = Globals()
    app.run(host='0.0.0.0', port=80)
