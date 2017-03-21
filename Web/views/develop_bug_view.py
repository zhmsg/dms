#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, jsonify, send_from_directory, g
from flask_login import current_user
from werkzeug.utils import secure_filename

from Web import bug_url_prefix, data_dir, create_blue
from Web import control
from Class import TIME_FORMAT_STR

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = bug_url_prefix
html_dir = "/BUG"

develop_bug_view = create_blue('develop_bug_view', url_prefix=url_prefix)

bug_status_desc = [u"等待问题确认", u"已有问题疑似拥有者", u"已确认问题拥有者", u"问题已被修复", u"问题被取消", u"现象正常"]


def ref_bug_no(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ref_key = "bug_no"
        if ref_key in request.args:
            g.bug_no = request.args[ref_key]
            return f(*args, **kwargs)
        elif "Referer" in request.headers:
            g.ref_url = request.headers["Referer"]
            find_result = re.findall(ref_key + "=([a-z\d]{32})", g.ref_url)
            if len(find_result) > 0:
                g.bug_no = find_result[0]
                return f(*args, **kwargs)
        if request.is_xhr is True:
            return jsonify({"status": False, "data": "Bad Request."})
        else:
            return "Bad Request"
    return decorated_function


@develop_bug_view.route("/", methods=["GET"])
def show_bug_list():
    if request.is_xhr is True:
        result, bug_list = control.get_bug_list(current_user.user_name, current_user.role)
        return jsonify({"status": result, "data": bug_list})
    my_bug_url = url_prefix + "/mine/"
    info_url = url_prefix + "/info/"
    new_link_role = "%s|%s" % (control.role_value["bug_new"], control.role_value["bug_link"])
    return render_template("%s/Show_BUG.html" % html_dir, bug_status_desc=control.bug_status_desc,
                           user_role=current_user.role, role_desc=control.role_value, url_prefix=url_prefix,
                           my_bug_url=my_bug_url, bug_level_desc=control.bug_level_desc, info_url=info_url,
                           new_link_role=new_link_role)


@develop_bug_view.route("/", methods=["POST"])
def new_bug():
    request_data = request.json
    bug_title = request_data["bug_title"]
    bug_level = request_data["bug_level"]
    result, bug_info = control.new_bug(current_user.user_name, current_user.role, bug_title, bug_level)
    if result is False:
        return jsonify({"status": False, "data": bug_info})
    bug_no = bug_info["bug_no"]
    return jsonify({"status": True, "data": "success", "location": url_prefix + "/info?bug_no=%s" % bug_no})


@develop_bug_view.route("/mine/", methods=["GET"])
def show_my_bug_list():
    result, bug_list = control.get_my_bug_list(current_user.user_name, current_user.role)
    return jsonify({"status": result, "data": bug_list})


@develop_bug_view.route("/statistic/", methods=["GET"])
def get_statistic():
    result, sta_info = control.get_bug_statistic(current_user.role)
    return jsonify({"status": result, "data": sta_info})


@develop_bug_view.route("/info/", methods=["GET"])
@ref_bug_no
def get_bug_info_func():
    bug_no = request.args["bug_no"]
    result, bug_info = control.get_bug_info(current_user.role, bug_no)
    if request.is_xhr is True:
        return jsonify({"status": result, "data": bug_info})
    if result is False:
        return bug_info
    result, user_list = control.get_role_user(control.role_value["bug_link"])
    if result is False:
        return user_list
    url_link_user = url_prefix + "/link/"
    url_bug_reason = url_prefix + "/reason/"
    url_example = url_prefix + "/example/"
    return render_template("%s/BUG_Info.html" % html_dir, bug_info=bug_info, bug_status_desc=bug_status_desc,
                           bug_no=bug_no,
                           user_role=current_user.role, current_user=current_user.user_name,
                           role_desc=control.role_value,
                           user_list=user_list, url_prefix=url_prefix, url_link_user=url_link_user,
                           url_bug_reason=url_bug_reason, url_example=url_example)


@develop_bug_view.route("/link/", methods=["GET"])
@ref_bug_no
def get_bug_link_func():
    exec_r, bug_links = control.get_bug_link(g.user_name, g.user_role, g.bug_no)
    return jsonify({"status": exec_r, "data": bug_links})


@develop_bug_view.route("/example/", methods=["GET"])
@ref_bug_no
def get_example():
    result, example_info = control.get_bug_example(current_user.user_name, current_user.role, g.bug_no)
    if result is False:
        return example_info
    return jsonify({"status": result, "data": example_info})


@develop_bug_view.route("/example/", methods=["POST"])
@ref_bug_no
def add_example():
    str_example = request.json["example"]
    result, example_info = control.add_bug_example(current_user.user_name, current_user.role, g.bug_no, str_example)
    if result is False:
        return example_info
    return jsonify({"status": result, "data": example_info})


@develop_bug_view.route("/<bug_no>/ys/", methods=["POST"])
def add_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.add_bug_link(bug_no, current_user.user_name, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["POST"])
def add_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.add_bug_link(bug_no, current_user.user_name, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/fix/", methods=["POST"])
def add_fix_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.user_name, current_user.role, current_user.user_name,
                                             "fix")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/cancel/", methods=["POST"])
def add_cancel_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.user_name, current_user.role, current_user.user_name,
                                             "cancel")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/design/", methods=["POST"])
def add_design_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.user_name, current_user.role, current_user.user_name,
                                             "design")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/ys/", methods=["DELETE"])
def del_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.delete_bug_link(bug_no, current_user.user_name, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["DELETE"])
def del_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.delete_bug_link(bug_no, current_user.user_name, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/reason/", methods=["GET"])
@ref_bug_no
def get_bug_reason():
    bug_no = g.bug_no
    exec_r, bug_reasons = control.get_bug_reason(g.user_name, g.user_role, bug_no)
    return jsonify({"status": exec_r, "data": bug_reasons})


@develop_bug_view.route("/reason/", methods=["POST", "PUT"])
@ref_bug_no
def add_bug_reason():
    bug_no = g.bug_no
    bug_reason = request.json["bug_reason"]
    if request.method == "POST":
        exec_r, bug_reasons = control.add_bug_reason(g.user_name, g.user_role, bug_no, bug_reason)
    else:
        exec_r, bug_reasons = control.update_bug_reason(g.user_name, g.user_role, bug_no, bug_reason)
    return jsonify({"status": exec_r, "data": [bug_reasons]})