#! /usr/bin/env python
from models import db, try_flush_session
import datetime


# { token : { "username": username, "ttl" : ttl,
# ... }
TokenDB = {}


def remove_token(token):
    if token in TokenDB.keys():
        del TokenDB[token]
        return True
    return False


def check_for_token_exists(token):
    if token in TokenDB.keys():
        return True
    return False


def generate_token(username):
    # TODO generate token
    # save it in memory (or DB?) (or in memory db?)
    token = "123456"
    # ttl for 14 days
    today = datetime.date.today()
    delta14days = datetime.timedelta(14)
    ttl = today + delta14days
    TokenDB[token] = {"username": username, "ttl": ttl}
    return token


def auth_is_valid(username, password):
    # hardcoded for testing
    if username == 'admin' and password == 'admin':
        return True
    return False


def isNewTask(submitDataId):
    if submitDataId == -1:
        return True
    return False


def conditionalUpdateTaskWithSubmitDataIfExists(taskObject, dataToProcess):
    """checks if the data to be submitted contains data in the keys specific to the task table
if so, adds them to the task object
return newly updated task object"""
    if 'priority' in dataToProcess.keys() and dataToProcess['priority'] != "":
        taskObject.priority = dataToProcess['priority']
    if 'deadline' in dataToProcess.keys() and dataToProcess['deadline'] != "":
        taskObject.deadlineDate = dataToProcess['deadline']
    if 'tasklist' in dataToProcess.keys() and dataToProcess['tasklist'] != "":
        taskObject.projectId = dataToProcess['tasklist']
    # it title is empty, the key will not exist in the json POST
    if 'title' in dataToProcess.keys() and dataToProcess['title'] != "":
        taskObject.title = dataToProcess['title']
    # description can not be NULL, empty string is OK
    if 'description' in dataToProcess.keys() and dataToProcess['description'] != "":
        taskObject.description = dataToProcess['description']
    if 'responsible' in dataToProcess.keys() and dataToProcess['responsible'] != "":
        taskObject.memberId = dataToProcess['responsible']
    return taskObject


def createNewTask(submitData):
    newTask = db.task()
    newTask = conditionalUpdateTaskWithSubmitDataIfExists(newTask, submitData)
    db.session.add(newTask)
    if try_flush_session() == 0:
        db.session.refresh(newTask)
        return newTask.itemId
    return -1


def updateExistingTask(submitData):
    taskToModify = db.session.query(db.task).filter(db.task.itemId == submitData['id']).one()
    taskToModify = conditionalUpdateTaskWithSubmitDataIfExists(taskToModify, submitData)
    db.session.add(taskToModify)
    if try_flush_session() == 0:
        return submitData['id']
    return -1


def check_token_username_combination(username, token):
    if token in TokenDB.keys():
        if TokenDB[token]["username"] == username:
            if datetime.date.today() < TokenDB[token]['ttl']:
                return True
    return False

