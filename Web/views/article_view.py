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
    return rt.render("add.html")


@article_view.route("/", methods=["POST"])
def add_article_action():
    request_data = request.json
    title = request_data["title"]
    abstract = request_data["abstract"]
    content = request_data["content"]
    exec_r, data = control.new_article(g.user_name, g.user_role, title, abstract, content)
    return jsonify({"status": exec_r, "data": data})
