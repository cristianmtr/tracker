#! /usr/bin/env python
from flask import Flask, render_template, jsonify, request, session
from models import db, try_flush_session, build_priority_id_to_name,\
    build_tasklist_id_to_name, build_user_id_to_name, check_token_username_combination
import logging
from logging.handlers import RotatingFileHandler
import json
from functools import wraps
from post import isNewTask, conditionalUpdateTaskWithSubmitDataIfExists,\
    updateExistingTask, createNewTask


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def is_loggedin(f):
    """checks if the user is logged in"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        # TODO actual check
        if token == "123456":
            return f(*args, **kwargs)
        else:
            return jsonify(data=-2)
    return wrapper


@app.route("/comments/<taskid>", methods=["POST", "GET"])
def comments(taskid):
    # comments = ['comment 1', 'comment 2', 'comment 3']
    commentsDb = db.session.query(db.comment).filter(db.comment.itemId==taskid).all()
    comments = []
    for comm in commentsDb:
        newComm = {}
        newComm["author_id"] = comm.memberId
        newComm["postDate"] = comm.postDate
        newComm["body"] = comm.body
        comments.append(newComm)
    return jsonify(data=comments)


@app.route("/logout", methods=["POST", "GET"])
@is_loggedin
def logout():
    if request.method == 'POST':
        del session['username']
        return jsonify(data="success")
    else:
        return "nothing to see here"


@app.route("/auth", methods=["POST"])
def cookie():
    if request.method == 'POST':
        submit_data = request.get_json()
        # hardcoded for testing
        if submit_data['username'] == 'admin' and submit_data['password'] == 'admin':
            # same for token
            # TODO generate token
            # with TTL 14 days
            # save it in memory (or DB?) (or in memory db?)
            data = {
                "token": "123456",
                "username": submit_data['username']
            }
            return jsonify(code=200, data=data)
        return jsonify(code=422)


@app.route("/check", methods=["POST"])
def check():
    if request.method == "POST":
        submit_data = request.get_json()
        yes = check_token_username_combination(submit_data['username'], submit_data['token'])
        if yes:
            return jsonify(code=200)
        return jsonify(code=422)

    
@app.route("/history/<taskid>", methods=["POST","GET"])
def history(taskid):
    historyEntriesDb = db.session.query(db.history).filter(db.history.itemId==taskid).all()
    historyEntries = []
    for entry in historyEntriesDb:
        newEntry = {}
        newEntry["statusKey"] = entry.statusKey
        newEntry["memberId"] = entry.memberId
        newEntry["statusDate"] = entry.statusDate
        historyEntries.append(newEntry)
    return jsonify(data=historyEntries)


@app.route("/post", methods=["POST", "GET"])
@is_loggedin
def post():
    """if the submitData is assoc. with an existing task entry, we will get its id
if it's not, we get -1 instead for that id field
depending on the success of either creating or updating a task
returns ID of the newly created task (or updated) if successful
returns -1 if there was a problem
"""
    submitData = request.get_json()
    print '/post : server received data: {}'.format(json.dumps(submitData))
    idToUpdateInTable = -1
    if isNewTask(submitData['id']):
        idToUpdateInTable = createNewTask(submitData)
    else:
        idToUpdateInTable = updateExistingTask(submitData)
    return jsonify(data=idToUpdateInTable)


@app.route("/task/<taskid>")
def task(taskid):
    task = db.session.query(db.task, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId,db.task.priority, db.task.projectId).filter(db.task.itemId == taskid).one()
    data = {
        'title':task.title if task.title else None,
        'priority':task.priority if task.priority else None,
        'description':task.description.encode('utf-8')if task.description else None,
        'deadline':task.deadlineDate.isoformat() if task.deadlineDate else None,
        'tasklist':task.projectId if task.projectId else None,
        'responsible':task.memberId if task.memberId else None,
        'author':task.authorId if task.authorId else None,
    }
    return jsonify(data=data)


@app.route("/json/")
def jsonInit():
    data = []
    tasks = db.session.query(db.task, db.task.projectId, db.task.priority, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId).all()
    for t in tasks:
        this_task = {}

        this_task['DT_RowId'] = t.itemId
        
        this_task['title'] = t.title
        
        # keep formatting when displaying description
        this_task['description'] = t.description.encode('utf-8')
        
        # handle empty fields, for deadlineDate or member info
        this_task['deadline'] = t.deadlineDate.isoformat() if t.deadlineDate else None
        this_task['responsible'] = t.memberId if t.memberId != 0 else None
        this_task['author'] = t.authorId if t.authorId != 0 else None
        this_task['tasklist'] = t.projectId if t.projectId else None
        this_task['priority'] = t.priority if t.priority else None
        data.append(this_task)

        # uncomment the following for sample data when no db is available
        # 
        # data = [
        # ['<a id="edit1" data-toggle="modal" data-target="#createNewModal" data-target="#createNewModal">1</a>', "this is description", "2more", "responsible", "authorId"],
        # ['<button onclick="btnclick(this);">2</button>',"this is description nr 2", "2more", "responsible2", "authorId"],
        # ]
    dataSources = {
        'priority': build_priority_id_to_name(),
        'tasklist': build_tasklist_id_to_name(),
        'responsible': build_user_id_to_name(),
    }
    return jsonify(
        data=data,
        dataSources=dataSources
    )


if __name__ == "__main__":
    app.debug = True
    app.secret_key = "123456"
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    # db = Globals()
    app.run(host='0.0.0.0', port=80)
