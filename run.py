#! /usr/bin/python
from flask import Flask, render_template, jsonify
from models import create_session, create_task_object, create_user_object
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)


# will store db globals
class Globals(object):
    def __init__(self):
        self.session = create_session()
        self.task = create_task_object()
        self.user = create_user_object()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/json")
def json():
    data = [
        [
            "2",
            "adsadas",
            "2more",
            "moi",
            "you"
        ],
        [
            "3",
            "adsdasdasfasfas",
            "never",
            "Thor",
            "Hulk"
        ]
    ]

    return jsonify(data=data)


if __name__ == "__main__":
    app.debug = True
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    globals = Globals()
    app.run(host='0.0.0.0', port=5000)
