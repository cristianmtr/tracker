from flask import Flask, render_template, jsonify, request
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
import backend

app = Flask(__name__)
app.debug = True
app.secret_key = "123456"
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)


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
                if backend.check_for_token_exists(submit_data['auth']['token']):
                    return f(*args, **kwargs)
        return jsonify(code=401)

    return wrapper


@app.route("/notify", methods=["POST"])
@is_loggedin
def notify():
    submit_data = request.get_json()
    token = backend.get_username_from_token(submit_data['auth']['token'])
    username = backend.get_username_from_token(token)
    data = {
        "notifications": backend.get_notifications(username),
    }
    return jsonify(code=200, data=data)


@app.route("/comments/<taskid>", methods=["POST"])
def post_comment(taskid):
    # TODO
    return jsonify(code=500)


@app.route("/comments/<taskid>", methods=["GET"])
def get_comment(taskid):
    # comments = ['comment 1', 'comment 2', 'comment 3']
    commentsDb = backend.get_comments_from_taskid(taskid)
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
        if backend.check_token_username_combination(submit_data['username'], submit_data['token']):
            if backend.remove_token(submit_data['token']):
                return jsonify(code=200)
        return jsonify(code=400)
    else:
        return "nothing to see here"


@app.route("/auth", methods=["POST"])
def cookie():
    if request.method == 'POST':
        submit_data = request.get_json()
        if backend.auth_is_valid(submit_data['username'], submit_data['password']):
            token = backend.generate_token(submit_data['username'])
            data = {
                "token": token,
            }
            return jsonify(code=200, data=data)
        return jsonify(code=422)


@app.route("/check", methods=["POST"])
def check():
    if request.method == "POST":
        submit_data = request.get_json()
        if 'username' in submit_data.keys() and 'token' in submit_data.keys():
            if backend.check_token_username_combination(submit_data['username'], submit_data['token']):
                return jsonify(code=200)
        return jsonify(code=422)


@app.route("/history/<taskid>", methods=["POST"])
@is_loggedin
def post_history(taskid):
    # TODO
    return jsonify(code=500)


@app.route("/history/<taskid>", methods=["GET"])
def history(taskid):
    historyEntriesDb = backend.get_history_from_taskid(taskid)
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
    new_task_id = backend.createNewTask(submit_data['data'])
    return jsonify(code=200, data=new_task_id)


@app.route("/task/<taskid>", methods=["POST"])
@is_loggedin
def update_task(taskid):
    submit_data = request.get_json()
    rtn_code = backend.updateExistingTask(submit_data['data'], taskid)
    if rtn_code == taskid:
        return jsonify(code=200)
    return jsonify(code=500)


@app.route("/task/<taskid>", methods=["GET"])
def gettask(taskid):
    task = backend.get_task(taskid)
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


@app.route("/json")
def jsonInit():
    data = []
    tasks = backend.get_task()
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
        'priority': backend.build_priority_id_to_name(),
        'tasklist': backend.build_tasklist_id_to_name(),
        'responsible': backend.build_user_id_to_name(),
    }
    return jsonify(
        data=data,
        dataSources=dataSources
    )


# if __name__ == "__main__":
#     app.run(port=5000)
