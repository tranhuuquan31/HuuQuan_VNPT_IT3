from distutils.util import change_root
from sqlite3 import Date
from typing import Concatenate
from flask_pymongo import PyMongo
from flask import request, jsonify, make_response
from library.extension import db, mail
from library.library_ma import  SchemaNews, CustomerNews
from flask import current_app, g
from werkzeug.local import LocalProxy
import jwt
from datetime import datetime
from functools import wraps
from datetime import datetime
import uuid
from itertools import chain
import imgbbpy

news_schema = SchemaNews()
news_schemas = SchemaNews(many= True)
# get_category_schemas = SchemagetCategory(many=True)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)

def add_news_service():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = request.json
        data = CustomerNews().load(data)
        token_decode = jwt.decode(token, 'member', algorithms='HS256')
        if data and ("title" in data) and ("name_category" in data) and ("URL" in data) and ("status" in data):
            title = data["title"]
            name_category = data["name_category"]
            URL_local = data["URL"]
            status = data["status"]
            client = imgbbpy.SyncClient('f27f4dff286642132235d3ae1eb5c7dc')
            image = client.upload(file=URL_local)
            URL = image.url
            time = datetime.now()
            news = {
                "id_member": token_decode["public_id"],
                "id_news": str(uuid.uuid4()),
                "title" : title,
                "name_category" : name_category,
                "URL_local": URL_local,
                "URL": URL,
                "status": status,
                "time" : time
            }
            try:
                db.news.insert_one(news)
                return "Thêm tin bài thành công!"
            except:
                return "Thêm tin bài thất bại!"
        else:
            return "Vùi lòng nhập đầy đủ !"

def edit_news_service(id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = request.json
        data = CustomerNews().load(data)
        token_decode = jwt.decode(token, 'member', algorithms='HS256')
        if data and ("title" in data) and ("name_category" in data) and ("URL" in data) and ("status" in data):
            news = {"id_news" : id}
            time = datetime.now()
            new_news = { "$set": {
                "id_member": token_decode["public_id"],
                "title" : data["title"],
                "name_category" : data["name_category"],
                "URL_local": data["URL"],
                "status": data["status"],
                "time" : time
            }}
            try:
                db.news.update_one(news, new_news)
                return "Cập nhật tin bài thành công!"
            except: 
                return "Cập nhật tin bài không thành công!"
        else:
            return "Vùi lòng nhập đầy đủ !"

def detail_news_service(id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = db.news.find_one({"id_news": id})
        if data:
            return news_schema.jsonify(data)
        else:
            return "Không tìm thấy tin bài!"
    else:
        return "Vui lòng đăng nhập để tiếp tục!"

def delete_news_service(id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = db.news.find_one({"id_news": id})
        if data:
            db.news.delete_one(data)
            return "Xóa thành công tin bài!"
        else:
            return "Xóa  không thành công tin bài"
    else:
        return "Vui lòng đăng nhập để tiếp tục!"
