#! /usr/bin/python
from flask import Flask, render_template, jsonify
from models import create_session, create_task_object, create_user_object

app = Flask(__name__)

# will store db globals
class Globals(object):
    def __init__(self):
        self.session = create_session()
        self.task = create_task_object()
        self.user = create_user_object()

globals = Globals()
        
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/json")
def json():
    data = [
        {'id':'2', 'description':'adasda', 'dead_line':'2more', 'responsible':'moi', 'author':'the other guy'},
        {'id':'3', 'description':'do that thing', 'dead_line':'never!', 'responsible':'Thor', 'author':'the other guy'},
    ]
    return jsonify(draw=1, recordsTotal=1, recordsFiltered=0, data=data)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
