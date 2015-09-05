from flask import Flask, render_template, jsonify, request
from models import db, build_priority_id_to_name,\
    build_tasklist_id_to_name, build_user_id_to_name
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
from backend import remove_token, check_for_token_exists,\
    updateExistingTask, createNewTask, check_token_username_combination, \
    auth_is_valid, generate_token, get_username_from_token, check_for_updates


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def is_loggedin(f):
    """checks if the user is logged in"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        submit_data = request.get_json()
        if "auth" in submit_data.keys():
            if "token" in submit_data['auth'].keys():
                if check_for_token_exists(submit_data['auth']['token']):
                    return f(*args, **kwargs)
        else:
            return jsonify(code=401)
    return wrapper


@app.route("/updates", methods=["POST"])
@is_loggedin
def updates():
    import pdb
    pdb.set_trace()
    submit_data = request.get_json()
    username = get_username_from_token(submit_data['auth']['token'])
    data = {
        "updates_list": check_for_updates(username),
    }
    return jsonify(code=200, data=data)


@app.route("/comments/<taskid>", methods=["POST"])
def post_comment(taskid):
    # TODO
    return jsonify(code=500)


@app.route("/comments/<taskid>", methods=["GET"])
def get_comment(taskid):
    # comments = ['comment 1', 'comment 2', 'comment 3']
    commentsDb = db.session.query(db.comment).filter(db.comment.itemId == taskid).all()
    comments = []
    for comm in commentsDb:
        newComm = {}
        newComm["author_id"] = comm.memberId
        newComm["postDate"] = comm.postDate
        newComm["body"] = comm.body
        comments.append(newComm)
    return jsonify(code=200, data=comments)


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == 'POST':
        submit_data = request.get_json()
        if check_token_username_combination(submit_data['username'], submit_data['token']):
            if remove_token(submit_data['token']):
                return jsonify(code=200)
        return jsonify(code=400)
    else:
        return "nothing to see here"


@app.route("/auth", methods=["POST"])
def cookie():
    if request.method == 'POST':
        submit_data = request.get_json()
        if auth_is_valid(submit_data['username'], submit_data['password']):
            token = generate_token(submit_data['username'])
            data = {
                "token": token,
                "username": submit_data['username']
            }
            return jsonify(code=200, data=data)
        return jsonify(code=422)


@app.route("/check", methods=["POST"])
def check():
    if request.method == "POST":
        submit_data = request.get_json()
        if 'username' in submit_data.keys() and 'token' in submit_data.keys():
            if check_token_username_combination(submit_data['username'], submit_data['token']):
                return jsonify(code=200)
        return jsonify(code=422)


@app.route("/history/<taskid>", methods=["POST"])
@is_loggedin
def post_history(taskid):
    # TODO
    return jsonify(code=500)


@app.route("/history/<taskid>", methods=["GET"])
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


@app.route("/task/", methods=["POST"])
@is_loggedin
def post_new_task():
    submit_data = request.get_json()
    new_task_id = createNewTask(submit_data['data'])
    return jsonify(code=200, data=new_task_id)


@app.route("/task/<taskid>", methods=["POST"])
@is_loggedin
def update_task(taskid):
    submit_data = request.get_json()
    updateExistingTask(submit_data['data'], taskid)
    return jsonify(code=200)


@app.route("/task/<taskid>", methods=["GET"])
def gettask(taskid):
    task = db.session.query(db.task, db.task.itemId, db.task.title, db.task.description, db.task.deadlineDate, db.task.memberId, db.task.authorId,db.task.priority, db.task.projectId).filter(db.task.itemId == taskid).one()
    data = {
        'title': task.title if task.title else None,
        'priority': task.priority if task.priority else None,
        'description': task.description.encode('utf-8') if task.description else None,
        'deadline': task.deadlineDate.isoformat() if task.deadlineDate else None,
        'tasklist': task.projectId if task.projectId else None,
        'responsible': task.memberId if task.memberId else None,
        'author': task.authorId if task.authorId else None,
    }
    return jsonify(code=200, data=data)


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
    app.run(host='0.0.0.0', port=5000)
