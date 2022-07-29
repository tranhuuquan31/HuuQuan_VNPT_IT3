from cgitb import html
from crypt import methods
from textwrap import wrap
from flask import Blueprint, render_template, request
from .services import add_category_service, edit_category_service, detail_category_service, delete_category_service, get_category_service

category = Blueprint("category", __name__)

@category.route("/add_category", methods = ["POST"])
def add_category():
    return add_category_service()

@category.route("/get_category", methods = ["GET", "POST"])
def get_category():
    return get_category_service()

@category.route("/edit_category/<id>", methods = ["PUT"])
def edit_category(id):
    return edit_category_service(id)

@category.route("/detail_category/<id>", methods = ["GET"])
def detail_category(id):
    return detail_category_service(id)

@category.route("/delete_category/<id>", methods = ["DELETE"])
def delete_category(id):
    return delete_category_service(id)