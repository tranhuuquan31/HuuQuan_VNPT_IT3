from flask import Flask, request, Blueprint
from .extension import db, ma, mail
from library.sign_up.controller import members
from library.category_manager.controller import category
from library.news_manager.controller import news
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from datetime import datetime, timedelta
from flask.json import JSONEncoder

# def create_db():
#     if not os.path.exists("library/member.db"):
#         db.create_all(app=app)
#         print("Created db!")
class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app(config_file = "config.py"):
    app = Flask(__name__)
    ma.init_app(app)
    app.json_encoder = MongoJsonEncoder
    app.config.from_pyfile(config_file)
    db.init_app(app)
    mail.init_app(app)
    app.register_blueprint(members)
    app.register_blueprint(category)
    app.register_blueprint(news)
    return app