import models
import datetime
import redis

DATE_FORMAT = "%a %b %d %H:%M:%S %Y"

db = models.Globals()

# 0 - tokens
# 1 - last_time_checked_DB
# 2 - notifications
TOKENS = redis.Redis('localhost', db=0)
LTC = redis.Redis('localhost', db=1)
NOTIFICATIONS = redis.Redis('localhost', db=2)


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
    if db.try_flush_session() == 0:
        db.session.refresh(newTask)
        new_notification("new_task", newTask.itemId)
        return newTask.itemId
    return -1


def updateExistingTask(submitData, task_id):
    taskToModify = db.session.query(db.task).filter(db.task.itemId == task_id).one()
    taskToModify = conditionalUpdateTaskWithSubmitDataIfExists(taskToModify, submitData)
    db.session.add(taskToModify)
    if db.try_flush_session() == 0:
        new_notification("task", task_id)
        return task_id
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


def get_notifications(username):
    # ltc - LAST TIME CHECKED
    # the last datetime.datetime the user checked for notifications
    notifications = []
    ltc = None
    ltc_string = LTC.get(username)
    if ltc_string:
        ltc = string_to_datetime(ltc_string)
    for timestamp in NOTIFICATIONS.keys():
        if ltc is None or string_to_datetime(timestamp) > ltc:
            notifications.append(NOTIFICATIONS.hgetall(timestamp))
    ltc_now = datetime.datetime.today()
    ltc_now_string = datetime_to_string(ltc_now)
    LTC.set(username, ltc_now_string)
    return notifications


def new_notification(event_type, unique_id):
    time_of_creation = datetime.datetime.today()
    time_of_creation_string = datetime_to_string(time_of_creation)
    print "notification {}: {} {}".format(time_of_creation_string, event_type, unique_id)
    NOTIFICATIONS.hmset(time_of_creation_string, {"type": event_type, "id": unique_id})
    return


def get_comments_from_taskid(taskid):
    return db.session.query(db.comment.body, db.comment.memberId, db.comment.postDate, db.comment.lastChangeDate).\
        filter(db.comment.itemId == taskid).order_by(db.comment.postDate).all()[::-1]


def get_history_from_taskid(taskid):
    return db.session.query(db.history.memberId, db.history.statusDate, db.history.statusKey).\
        filter(db.history.itemId == taskid).order_by(db.history.statusDate).all()[::-1]


def get_task(taskid=None):

    """

    :param taskid: the id of the task. if None or not passed, will return all tasks
    :return:
    """
    if taskid:
        return db.session.query(db.task, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId,db.task.priority, db.task.projectId).filter(db.task.itemId == taskid).one()
    else:
        return db.session.query(db.task, db.task.projectId, db.task.priority, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId).all()


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
