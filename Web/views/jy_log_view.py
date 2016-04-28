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
    result, info = control.look_jy_log(current_user.account, current_user.role, 1, 0, 0)
    if result is False:
        return info
    return render_template("%s/Show_Log.html" % html_dir, log_list=info, url_prefix=url_prefix)


@jy_log_view.route("/", methods=["POST"])
@login_required
def new_action_role():
    if "Referer" not in request.headers:
        return "Bad Request"
    ref_url = request.headers["Referer"]
    find_module = re.findall("\?module_no=([0-9]+)", ref_url)
    if len(find_module) < 0:
        return "Bad Request."
    module_no = int(find_module[0])
    action_desc = request.form["action_desc"]
    min_role = request.form["min_role"]
    result, info = control.new_right_action(current_user.account, current_user.role, module_no, action_desc, min_role)
    if result is False:
        return info
    return redirect(ref_url)
