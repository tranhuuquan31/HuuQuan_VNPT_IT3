from types import MemberDescriptorType
from flask_pymongo import PyMongo
from flask import request, jsonify, Flask, session, make_response
from library.extension import db, mail
from library.library_ma import Schema, CustomerSchema
import random
from flask_mail import Message
from flask import current_app, g
from werkzeug.local import LocalProxy
from  werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps


member_schema = Schema()
members_schema = Schema(many= True)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

db = LocalProxy(get_db)

def signup_service():
    data = request.json
    data = CustomerSchema().load(data)
    if (data and ('user_name' in data) and ('password' in data) and ('repeat_password' in data) and ('email' in data)):
        if db.member.find_one({"user_name" : data["user_name"]}) or db.member.find_one({"email" : data["email"]}):
            return "Tên đăng nhập hoặc email đã tồn tại"
        elif data["password"] == data["repeat_password"]:
            user_name = data["user_name"]
            password = generate_password_hash(data["password"])
            email = data["email"]
            member = {
                "public_id" : str(uuid.uuid4()),
                "user_name" : user_name,
                "password": password,
                "email": email
            }
            try:
                db.member.insert_one(member)
                return "Bạn đã tạo tài khoản thành công"
            except:
                return "Lỗi không thể tạo tài khoản"
        else:
            return "Mật khẩu xác nhận không đúng"
    else:
        return "Vui lòng nhập đầy đủ thông tin "
def token_required(f):
    @wraps
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, "member")
            current_user = db.member.find({"public_id" : data["public_id"]})
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
    return decorated

def signin_service():
    data = request.json
    data = CustomerSchema().load(data)
    member = db.member.find_one({"user_name" : data["user_name"]})
    if data and ('user_name' in data) and ('password' in data):
        if data["user_name"] == member["user_name"]:
            # global user_name_signin 
            # user_name_signin = data["user_name"]
            if check_password_hash(member["password"], data["password"]):
                token = jwt.encode({
                    'public_id': member["public_id"],
                    'exp' : datetime.utcnow() + timedelta(minutes = 30)
                }, 'member', algorithm='HS256')
                return make_response(jsonify({'token' : token.encode().decode('UTF-8')}), 201)
            else:
                return make_response(
                    'Mật khẩu không chính xác',
                    403,
                    {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'})
        else: 
            return "Tên đăng nhập không đúng, vui lòng thử lại"
    else:
        return "Vui lòng nhập nhập đầy đủ tên đăng nhập và mật khẩu"
        
def logout_service():
    token = None
    # jwt is passed in the request header
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    # return 401 if token is not passed
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    db.blacklist_token.insert_one({"token" : token})
    return "Dang xuat thanh cong"


def forget_password_service():
    data = request.json
    if data:
        global user_name_forget
        user_name_forget = data["user_name"]
        member = db.member.find_one({"user_name" : data["user_name"]})
        print(member)
        if member: 
            global number 
            number = random.randint(100000, 999999)
            email = member["email"]
            title_mail = "Xác thực tài khoản"
            msg = Message(title_mail, sender='huuphuongtp2@gmail.com', recipients=[email])
            message_email = "Mã xác nhận 6 chữ số của bạn là: {} ".format(number)
            msg.body = message_email
            try: 
                mail.send(msg)
                return "Gửi email xác nhận thành công!"
            except:
                return "Gửi email xác nhận không thành công!"
        else:
            return "Tên người dùng không đúng!"
    else:
        return "Vui lòng nhập tên người dùng"

def very_acc_service():
    data = request.json
    if data:
        number_very = data["number_very"]
        if number_very == str(number):
            return "Mã xác nhận chính xác "
        else: return "Mã xác nhận không chính xác"
    else:
        return "Vui lòng nhập mã xác thực "


def reset_password_service():
    data = request.json
    member_query = {"user_name": user_name_forget}
    if data and "password" in data and "repeat_password" in data:
        new_member = {"$set": {"password" : generate_password_hash(data["password"])}}
        try:
            db.member.update_one(member_query, new_member)
            return "Cập nhật mật khẩu thành công"
        except:
            return "Cập nhật mật khẩu không thành công"
    else:
        return "Vui lòng nhập mật khẩu và nhập  lại mật khẩu"


def acc_information_service():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return jsonify({'message' : 'Token is missing !!'}), 401
    if not db.blacklist_token.find_one({"token": token}):
        try:
            # # decoding the payload to fetch the stored details
            data = jwt.decode(token, 'member', algorithms='HS256')
            current_user = db.member.find_one({"public_id" : data["public_id"]})
            if current_user:
                data = request.json
                member_query = {"public_id": current_user["public_id"]}
                if data and "email" in data:
                    if not db.member.find_one({"email" : data["email"]}):
                        new_email = {"$set": {"email": data["email"]}}
                        try:
                            db.member.update_one(member_query, new_email)
                            return "Cập nhật email thành công"
                        except:
                            return "Cập nhật email không thành công"
                    else:
                        return "Email đã tồn tại"
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
    else:
        return "vui lòng đăng nhập để tiếp tục "




