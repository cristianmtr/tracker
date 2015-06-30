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


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/json")
def json():
    data = []
    tasks = globals.session.query(globals.task, globals.task.itemId, globals.task.description, globals.task.deadlineDate, globals.task.memberId, globals.task.authorId).all()
    for t in tasks:
        data.append([t.itemId, "<pre>" + t.description + "</pre>", t.deadlineDate.isoformat() if t.deadlineDate != None else None, t.memberId, t.authorId])
    return jsonify(data=data)


if __name__ == "__main__":
    app.debug = True
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    globals = Globals()
    app.run(host='0.0.0.0', port=5000)
