#! /usr/bin/python
from flask import Flask, render_template, jsonify, request
from models import create_session, create_task_object, create_user_object, create_tasklist_object
import logging
from logging.handlers import RotatingFileHandler
import json

app = Flask(__name__)


class Globals(object):
    """Will store db globals"""

    def __init__(self):
        self.session = create_session()
        self.task = create_task_object()
        self.user = create_user_object()
        self.tasklist = create_tasklist_object()
        self.user_id_to_name = {}
        self.build_user_id_to_name()

    def build_user_id_to_name(self):
        users = self.session.query(self.user, self.user.memberId, self.user.firstName).all()
        for u in users:
            self.user_id_to_name[u.memberId] = u.firstName


@app.route("/")
def index():
    return render_template('index.html')


def isNewTask(submitDataId):
    if submitDataId == -1:
        return True
    return False


def createNewTask(submitData):
    newTask = db.task(
        priority = submitData['priority'],
        deadlineDate = submitData['deadline'],
        projectId = submitData['tasklist'],
        title = submitData['title'],
        description = submitData['description'],
        memberId = submitData['responsible'],
    )
    db.session.add(newTask)
    db.session.flush()
    db.session.refresh(newTask)
    return newTask.itemId


def updateExistingTask(submitData):
    taskToModify = db.session.query(db.task).filter(db.task.itemId==submitData['id']).one()
    taskToModify.priority = submitData['priority']
    taskToModify.deadlineDate = submitData['deadline']
    taskToModify.projectId = submitData['tasklist']
    taskToModify.title = submitData['title']
    taskToModify.description = submitData['description']
    taskToModify.memberId = submitData['responsible']
    db.session.add(taskToModify)
    db.session.flush()
    return


@app.route("/post", methods=["POST", "GET"])
def post():
    submitData = request.get_json()
    print '/post : server received data: {}'.format(json.dumps(submitData))
    idToUpdateInTable = submitData['id']
    if isNewTask(submitData['id']):
        idToUpdateInTable = createNewTask(submitData)
    else:
        updateExistingTask(submitData)
    return jsonify(data=idToUpdateInTable)


@app.route("/json/<taskid>")
def jsontask(taskid):
    task = db.session.query(db.task, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId,db.task.priority, db.task.projectId).filter(db.task.itemId == taskid).one()
    data = {
        'title':task.title if task.title else None,
        'priority':task.priority if task.priority else None,
        'description':task.description.encode('utf-8') if task.description else None,
        'deadline':task.deadlineDate.isoformat() if task.deadlineDate else None,
        'tasklist':task.projectId if task.projectId else None,
        'responsible':task.memberId if task.memberId else None,
        'author':task.authorId if task.authorId else None,
    }
    return jsonify(data=data)


@app.route("/json/")
def jsonall():
    data = []
    tasks = db.session.query(db.task, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId).all()
    for t in tasks:
        this_task = {}

        this_task['DT_RowId'] = t.itemId
        
        this_task['title'] = t.title
        
        # keep formatting when displaying description
        this_task['description'] = '<pre>{}</pre>'.format(t.description.encode('utf-8'))
        
        # handle empty fields, for deadlineDate or member info
        this_task['deadline'] = t.deadlineDate.isoformat() if t.deadlineDate else None
        this_task['responsible'] = db.user_id_to_name[t.memberId] if t.memberId != 0 else None
        this_task['author'] = db.user_id_to_name[t.authorId] if t.authorId != 0 else None
        data.append(this_task)

        # uncomment the following for sample data when no db is available
        # 
        # data = [
        # ['<a id="edit1" data-toggle="modal" data-target="#createNewModal" data-target="#createNewModal">1</a>', "this is description", "2more", "responsible", "authorId"],
        # ['<button onclick="btnclick(this);">2</button>',"this is description nr 2", "2more", "responsible2", "authorId"],
        # ]
        
    tasklists_dict = {}
    all_tasklists = db.session.query(db.tasklist, db.tasklist.projectId, db.tasklist.name).all()
    for tsklst in all_tasklists:
        tasklists_dict[tsklst.projectId] = tsklst.name
        dataSources = {
            'priority':{
                1: 'Urgent',
                2: 'Medium',
                3: 'Low',
            },
            'tasklist': tasklists_dict,
            'responsible':db.user_id_to_name,
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
