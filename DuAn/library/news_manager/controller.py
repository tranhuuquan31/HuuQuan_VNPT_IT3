from cgitb import html
from crypt import methods
from textwrap import wrap
from flask import Blueprint
from .services import add_news_service, edit_news_service, delete_news_service, detail_news_service

news = Blueprint("news", __name__)

@news.route("/add_news", methods = ["POST"])
def add_news():
    return add_news_service()

@news.route("/edit_news/<id>", methods = ["PUT"])
def edit_news(id):
    return edit_news_service(id)

@news.route("/detail_news/<id>", methods = ["GET"])
def detail_news(id):
    return detail_news_service(id)

@news.route("/delete_news/<id>", methods = ["DELETE"])
def delete_news(id):
    return delete_news_service(id)