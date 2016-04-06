#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from flask import Blueprint, render_template, request, redirect,jsonify, send_from_directory
from flask_login import login_required, current_user

from Web import right_url_prefix as url_prefix
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/RIGHT"

develop_right_view = Blueprint('develop_right_view', __name__)


@develop_right_view.app_errorhandler(500)
def handle_500(e):
    print(e.args)
    return str(e.args)


@develop_right_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_right_view.route("/", methods=["GET"])
@login_required
def show_module_list():
    result, info = control.get_right_module(current_user.role)
    if result is False:
        return info
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
        result, module_role_info = control.get_right_module_role(current_user.role, module_no)
        if result is False:
            return module_role_info
        result, action_list = control.get_right_action_role(current_user.role, module_no)
        if result is False:
            return action_list
        return render_template("%s/right_module.html" % html_dir, module_list=info, url_prefix=url_prefix,
                               module_role_info=module_role_info, action_list=action_list)
    return render_template("%s/right_module.html" % html_dir, module_list=info, url_prefix=url_prefix)


@develop_right_view.route("/", methods=["POST"])
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