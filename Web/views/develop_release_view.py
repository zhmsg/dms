#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, g
from Web import release_url_prefix as url_prefix, create_blue, user_blacklist
from Web.views import control


sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Release"


develop_release_view = create_blue('develop_release_view', url_prefix=url_prefix)


@develop_release_view.before_request
def before_request():
    now_time = datetime.now()
    now_hour = now_time.hour
    now_minute = now_time.minute
    if now_hour in [9, 10, 11, 14, 15, 16, 17] and 10 <= now_minute <= 20:
        g.release_period = True
    else:
        g.release_period = False
        allow_url = [url_prefix + "/", url_prefix + "/task/"]
        if request.path not in allow_url:
            user_blacklist.append(g.user_name)
            return jsonify({"status": False, "data": u"非法时段"})


@develop_release_view.route("/", methods=["GET"])
def index_func():
    context = {}
    context["url_task_list"] = url_prefix + "/task/"
    return render_template("%s/Release_ih.html" % html_dir, **context)


@develop_release_view.route("/task/", methods=["GET"])
def list_task():
    result, info = control.get_task(g.user_name, g.user_role)
    return jsonify({"status": result, "data": info})
