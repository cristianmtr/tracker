#! /usr/bin/env python
from models import db, tryFlushSession


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
    if tryFlushSession() == 0:
        db.session.refresh(newTask)
        return newTask.itemId
    return -1


def updateExistingTask(submitData):
    taskToModify = db.session.query(db.task).filter(db.task.itemId == submitData['id']).one()
    taskToModify = conditionalUpdateTaskWithSubmitDataIfExists(taskToModify, submitData)
    db.session.add(taskToModify)
    if tryFlushSession() == 0:
        return submitData['id']
    return -1
