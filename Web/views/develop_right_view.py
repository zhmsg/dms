#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from flask import render_template, request, redirect
from flask_login import current_user

from Web import right_url_prefix as url_prefix, create_blue
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/RIGHT"

develop_right_view = create_blue('develop_right_view', url_prefix=url_prefix)


@develop_right_view.route("/", methods=["GET"])
def show_module_list():
    result, info = control.get_right_module(current_user.role)
    if result is False:
        return info
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
        result, module_role_info = control.get_right_module_role(current_user.role, module_no)
        if result is False:
            return module_role_info
        module_role_dict = {}
        for item in module_role_info:
            module_role_dict[item["module_role"]] = item
        result, action_list = control.get_right_action_role(current_user.role, module_no)
        if result is False:
            return action_list
        if current_user.role & control.role_value["right_new"] > 0:
            new_right = True
        else:
            new_right = False
        return render_template("%s/right_module.html" % html_dir, module_list=info, url_prefix=url_prefix,
                               module_role_info=module_role_info, action_list=action_list, new_right=new_right,
                               user_name=current_user.user_name, module_role_dict=module_role_dict)
    return render_template("%s/right_module.html" % html_dir, module_list=info, url_prefix=url_prefix)


@develop_right_view.route("/", methods=["POST"])
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
    result, info = control.new_right_action(current_user.user_name, current_user.role, module_no, action_desc, min_role)
    if result is False:
        return info
    return redirect(ref_url)


@develop_right_view.route("/action/delete/<int:action_no>/", methods=["GET"])
def del_action_role(action_no):
    if "Referer" not in request.headers:
        return "Bad Request"
    ref_url = request.headers["Referer"]
    result, info = control.delete_right_action(current_user.user_name, current_user.role, action_no)
    if result is False:
        return info
    return redirect(ref_url)