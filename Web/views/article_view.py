#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import os
import base64
from time import time
from random import randint
from datetime import datetime
from flask import request, send_from_directory, g, jsonify
from Tools.RenderTemplate import RenderTemplate
from Web import article_url_prefix as url_prefix, create_blue, control

rt = RenderTemplate("Article", url_prefix=url_prefix)
article_view = create_blue('article_view', url_prefix=url_prefix)


@article_view.route("/")
def add_func():
    article_no = ""
    if "article_no" in request.args:
        article_no = request.args["article_no"]
    if request.is_xhr is True:
        if len(article_no) != 32:
            return jsonify({"status": False, "data": "无效的编号"})
        exec_r, data = control.get_article(g.user_name, g.user_role, article_no)
        return jsonify({"statuys": exec_r, "data": data})
    return rt.render("add.html", article_no=article_no)


@article_view.route("/", methods=["POST"])
def add_article_action():
    request_data = request.json
    title = request_data["title"]
    abstract = request_data["abstract"]
    content = request_data["content"]
    exec_r, data = control.new_article(g.user_name, g.user_role, title, abstract, content)
    return jsonify({"status": exec_r, "data": data})


@article_view.route("/", methods=["PUT"])
def update_article_action():
    request_data = request.json
    article_no = request_data["article_no"]
    title = request_data["title"]
    abstract = request_data["abstract"]
    content = request_data["content"]
    exec_r, data = control.update_article(g.user_name, g.user_role, article_no, title, abstract, content)
    return jsonify({"status": exec_r, "data": data})
