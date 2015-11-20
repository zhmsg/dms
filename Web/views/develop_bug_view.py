#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'


develop_bug_view = Blueprint('develop_bug_view', __name__, url_prefix="/dev/bug")

bug_status_desc = [u"等待BUG确认", u"已有BUG疑似拥有者", u"已确认BUG拥有者", u"BUG已被修复", u"BUG被取消", u"BUG现象正常"]


@develop_bug_view.app_errorhandler(500)
def handle_500(e):
    print(e.args)
    return str(e.args)


@develop_bug_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_bug_view.route("/", methods=["GET"])
def show_bug_list():
    result, bug_list = control.get_bug_list(current_user.role)
    if result is False:
        return bug_list
    return render_template("/Dev/BUG/Show_BUG.html", bug_list=bug_list, bug_status_desc=bug_status_desc,
                           user_role=current_user.role, role_value=control.user_role)


@develop_bug_view.route("/info/", methods=["GET"])
def bug_info():
    if "bug_no" not in request.args:
        return u"请求错误"
    bug_no = request.args["bug_no"]
    result, bug_info = control.get_bug_info(current_user.role, bug_no)
    if result is False:
        return bug_info
    return render_template("/Dev/BUG/BUG_Info.html", bug_info=bug_info, bug_status_desc=bug_status_desc,
                           user_role=current_user.role, current_user=current_user.account, role_value=control.user_role)


@develop_bug_view.route("/new/", methods=["POST"])
def new_bug():
    bug_title = request.form["bug_title"]
    result, bug_info = control.new_bug(current_user.account, current_user.role, bug_title)
    if result is False:
        return bug_info

    bug_no = bug_info["bug_no"]
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)