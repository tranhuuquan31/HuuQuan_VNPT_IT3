from distutils.util import change_root
from sqlite3 import Date
from typing import Concatenate
from flask_pymongo import PyMongo
from flask import request, jsonify, make_response
from library.extension import db, mail
from library.library_ma import CustomerCategory, SchemaCategory, SchemagetCategory
from flask import current_app, g
from werkzeug.local import LocalProxy
import jwt
from datetime import datetime
from functools import wraps
from datetime import datetime
import uuid
from itertools import chain


category_schema = SchemaCategory()
category_schemas = SchemaCategory(many= True)
get_category_schemas = SchemagetCategory(many=True)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)

def add_category_service():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = request.json
        data = CustomerCategory().load(data)
        token_decode = jwt.decode(token, 'member', algorithms='HS256')
        if data and "name_category" in data and "category_code" in data:
            if  db.category.find_one({"category_code": data["category_code"]}):
                return "Tên chuyên mục hoặc mã chuyên mực đã tồn tại"
            else:
                name_category = data["name_category"]
                category_code = data["category_code"]
                if "parent_categoy" in data:
                    parent_category = data["parent_category"]
                else:
                    parent_category = ""
                if "status" in data:
                    status = data["status"]
                else:
                    status = ""
                time = datetime.now()
                category = {
                    "id_category" :str(uuid.uuid4()),
                    "id_member": token_decode["public_id"],
                    "name_category" : name_category,
                    "category_code" : category_code,
                    "parent_category": parent_category,
                    "status": status,
                    "time" : time
                }
                print(category)
                try: 
                    db.category.insert_one(category)
                    return "Thêm chuyên mục thành công"
                except:
                    return "Thêm chuyên mục thất bại"
        else:
            return "Vui lòng đầy đủ tên chuyên mục và mã số chuyên mục"
    else:
        return "vui lòng đăng nhập để tiếp tục "

def get_category_service():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = request.json
        if not "search" in data and not "start_date" in data and not "end_date" in data:
            return get_category_schemas.jsonify(db.category.find())
        if not "search" in data and "start_date" in data:
            if "end_date" in data:
                category = db.category.find({
                "time": {
                "$gt" :datetime.strptime(data["start_date"], '%Y-%m-%d'),
                "$lt" :datetime.strptime(data["end_date"],  '%Y-%m-%d')
                }
                })
                return get_category_schemas.jsonify(category)
            else:
                category = db.category.find({
                "time": {
                "$gt" :datetime.strptime(data["start_date"], '%Y-%m-%d'),
                "$lt" :datetime.now()
                }
                })
                return get_category_schemas.jsonify(category)
        if "search" in data:
            category_code = db.category.find({"category_code" : data["search"]})
            name_category = db.category.find({"name_category": data["search"]})
            if "start_date" in data:
                if "end_date" in data:
                    category = db.category.find({
                    "time": {
                    "$gt" :datetime.strptime(data["start_date"], '%Y-%m-%d'),
                    "$lt" :datetime.strptime(data["end_date"],  '%Y-%m-%d')
                    }
                    })
                else:
                    category = db.category.find({
                    "time": {
                    "$gt" :datetime.strptime(data["start_date"], '%Y-%m-%d'),
                    "$lt" :datetime.now()
                    }
                    })
                data_category = []
                for x in chain(category_code, name_category):
                    if x in category:
                        data_category.append(x)
                return get_category_schemas.jsonify(data_category)
            else:
                return get_category_schemas.jsonify(chain(category_code, name_category))
    else:
        return "Vui lòng đăng nhập để tiếp tục "


def edit_category_service(id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = request.json
        data = CustomerCategory().load(data)
        token_decode = jwt.decode(token, 'member', algorithms='HS256')
        if data and "name_category" in data and "category_code" in data:
            if db.category.find_one({"name_category": data["name_category"]}) or db.category.find_one({"category_code": data["category_code"]}):
                return "Tên chuyên mục hoặc mã chuyên mực đã tồn tại"
            else:
                if "parent_categoy" in data:
                    parent_category = data["parent_category"]
                else:
                    parent_category = ""
                if "status" in data:
                    status = data["status"]
                else:
                    status = ""
                if not db.category.find_one({"id_category": id}):
                    return "Không tìm thấy địa chỉ ID"
                category_query = {"id_category": id}
                time = datetime.now()
                new_category = {"$set": {"id_member": token_decode["public_id"],
                                         "name_category" : data["name_category"],
                                         "category_code": data["category_code"],
                                         "parent_category": data["parent_category"],
                                         "status" : data["status"],
                                         "time" : time
                }}
                try:
                    db.category.update_one(category_query, new_category)
                    return "Cập nhật chuyên mục thành công"
                except:
                    return "Cập nhật chuyên mục không thành công"
        else:
            return "Vui lòng đầy đủ tên chuyên mục và mã số chuyên mục"
    else:
        return "Vui lòng đăng nhập để tiếp tục "

def detail_category_service(id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = db.category.find_one({"id_category": id})
        if data:
            return category_schema.jsonify(data)
        else:
            return "Không tìm thấy chuyên mục"
    else:
        return "Vui lòng đăng nhập để tiếp tục "

def delete_category_service(id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        data = db.category.find_one({"id_category": id})
        if data:
            db.category.delete_one(data)
            return "Xóa chuyên mục thành công!"
        else:
            return "Không tìm thấy chuyên mục!"
    else:
        return "Vui lòng đăng nhập để tiếp tục "
