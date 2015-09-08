from models import db, try_flush_session
import datetime
import redis

DATE_FORMAT = "%a %b %d %H:%M:%S %Y"

# 0 - tokens
# 1 - last_time_checked_DB
# 2 - updates
TOKENS = redis.Redis('localhost', db=0)
LTC = redis.Redis('localhost', db=1)
UPDATES = redis.Redis('localhost', db=2)


def datetime_to_string(date_obj):
    return date_obj.strftime(DATE_FORMAT)


def string_to_datetime(string_obj):
    return datetime.datetime.strptime(string_obj, DATE_FORMAT)


def remove_token(token):
    if TOKENS.delete(token) == 1:
        return True
    return False


def check_for_token_exists(token):
    if TOKENS.hgetall(token) != {}:
        return True
    return False


def generate_token(username):
    # TODO generate token
    token = "123456"
    # ttl for 14 days
    today = datetime.date.today()
    delta14days = datetime.timedelta(14)
    ttl = today + delta14days
    ttl_format = datetime_to_string(ttl)
    TOKENS.hmset(token, {"username": username, "ttl": ttl_format})
    return token


def auth_is_valid(username, password):
    # hardcoded for testing
    if username == 'admin' and password == 'admin':
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
    if 'title' in dataToProcess.keys() and dataToProcess['title'] != "":
        taskObject.title = dataToProcess['title']
    if 'description' in dataToProcess.keys():
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
        new_update("new_task", newTask.itemId)
        return newTask.itemId
    return -1


def updateExistingTask(submitData, task_id):
    taskToModify = db.session.query(db.task).filter(db.task.itemId == task_id).one()
    taskToModify = conditionalUpdateTaskWithSubmitDataIfExists(taskToModify, submitData)
    db.session.add(taskToModify)
    if try_flush_session() == 0:
        return task_id
        new_update("task", task_id)
    return -1


def check_token_username_combination(username, token):
    if TOKENS.hgetall(token) != {}:
        if TOKENS.hget(token, "username") == username:
            ttl_string = TOKENS.hget(token, "ttl")
            ttl = string_to_datetime(ttl_string)
            if datetime.datetime.today() < ttl:
                return True
    return False


def get_username_from_token(token):
    name = TOKENS.hget(token, 'username')
    if name != {}:
        return name
    return None


def check_for_updates(username):
    # ltc - LAST TIME CHECKED
    # the last datetime.datetime the user checked for updates
    list_of_updates = []
    ltc = None
    ltc_string = LTC.get(username)
    if ltc_string:
        ltc = string_to_datetime(ltc_string)
    for timestamp in UPDATES.keys():
        if ltc is None or string_to_datetime(timestamp) > ltc:
            list_of_updates.append(UPDATES.hgetall(timestamp))
    ltc_now = datetime.datetime.today()
    ltc_now_string = datetime_to_string(ltc_now)
    LTC.set(username, ltc_now_string)
    return list_of_updates


def new_update(event_type, unique_id):
    time_of_creation = datetime.datetime.today()
    time_of_creation_string = datetime_to_string(time_of_creation)
    print time_of_creation_string
    UPDATES.hmset(time_of_creation_string, {"type": event_type, "id": unique_id})
    return