#! /usr/bin/env python
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


@app.route("/")
def index():
    return render_template('index.html')


def isNewTask(submitDataId):
    if submitDataId == -1:
        return True
    return False


def conditionalUpdateTaskWithSubmitDataIfExists(taskObject, dataToProcess):
    """checks if the data to be submitted contains data in the keys specific to the task table
if so, adds them to the task object
return newly updated task object"""
    if 'priority' in dataToProcess.keys():
        taskObject.priority = dataToProcess['priority']
    if 'deadline' in dataToProcess.keys():
        taskObject.deadlineDate = dataToProcess['deadline']
    if 'tasklist' in dataToProcess.keys():
        taskObject.projectId = dataToProcess['tasklist']
    if 'title' in dataToProcess.keys():
        taskObject.title = dataToProcess['title']
    if 'description' in dataToProcess.keys():
        taskObject.description = dataToProcess['description']
    if 'responsible' in dataToProcess.keys():
        taskObject.memberId = dataToProcess['responsible']
    return taskObject


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


def createNewTask(submitData):
    newTask = db.task()
    newTask = conditionalUpdateTaskWithSubmitDataIfExists(newTask, submitData)
    db.session.add(newTask)
    if tryFlushSession() == 0:
        db.session.refresh(newTask)
        return newTask.itemId
    return -1


def updateExistingTask(submitData):
    taskToModify = db.session.query(db.task).filter(db.task.itemId==submitData['id']).one()
    taskToModify = conditionalUpdateTaskWithSubmitDataIfExists(taskToModify, submitData)
    db.session.add(taskToModify)
    if tryFlushSession() == 0:
        return submitData['id']
    return -1


@app.route("/post", methods=["POST", "GET"])
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


@app.route("/json/<taskid>")
def jsontask(taskid):
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
def jsonall():
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
        'responsible':build_user_id_to_name(),
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
