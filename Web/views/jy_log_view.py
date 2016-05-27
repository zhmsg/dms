#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from Web import log_url_prefix as url_prefix
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/LOG"

jy_log_view = Blueprint('jy_log_view', __name__)


@jy_log_view.app_errorhandler(500)
def handle_500(e):
    print(e.args)
    return str(e.args)


@jy_log_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@jy_log_view.route("/", methods=["GET"])
@login_required
def show_log_list():
    if "start_time" in request.args and request.args["start_time"] != "":
        start_time = request.args["start_time"]
    else:
        start_time = None
    if "end_time" in request.args and request.args["end_time"] != "":
        end_time = request.args["end_time"]
    else:
        end_time = None
    if "log_level" in request.args and request.args["log_level"] != "all":
        level = request.args["log_level"]
    else:
        level = None

    if "url_prefix" in request.args and request.args["url_prefix"] != "":
        search_url = request.args["url_prefix"]
    else:
        search_url = ""
    if "account" in request.args and request.args["account"] != "":
        search_account = request.args["account"]
    else:
        search_account = ""
    if "look_before" in request.args and request.args["look_before"] == "1":
        look_before = True
    else:
        look_before = False
    result, info = control.look_jy_log(current_user.account, current_user.role, 1, 0, 0, look_before=look_before,
                                       level=level, search_url=search_url, search_account=search_account)
    if result is False:
        return info
    log_records = info["log_records"]
    start_time = int(info["require"]["start_time"])
    end_time = int(info["require"]["end_time"])
    return render_template("%s/Show_Log.html" % html_dir, log_list=log_records, url_prefix=url_prefix, look_before=look_before,
                           log_level=control.jy_log.log_level, current_level=level, search_url=search_url,
                           search_account=search_account, start_time=start_time, end_time=end_time)

