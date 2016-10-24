#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
from datetime import datetime
from flask import render_template, request, redirect,jsonify, send_from_directory
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

bug_status_desc = [u"等待BUG确认", u"已有BUG疑似拥有者", u"已确认BUG拥有者", u"BUG已被修复", u"BUG被取消", u"BUG现象正常"]


@develop_bug_view.route("/", methods=["GET"])
def show_bug_list():
    result, bug_list = control.get_bug_list(current_user.role)
    if result is False:
        return bug_list
    return render_template("%s/Show_BUG.html" % html_dir, bug_list=bug_list, bug_status_desc=bug_status_desc,
                           user_role=current_user.role, role_desc=control.role_value, url_prefix=url_prefix)


@develop_bug_view.route("/statistic/", methods=["GET"])
def get_statistic():
    result, sta_info = control.get_bug_statistic(current_user.role)
    return jsonify({"status": result, "data": sta_info})


@develop_bug_view.route("/info/", methods=["GET"])
def bug_info():
    if "bug_no" not in request.args:
        return u"请求错误"
    bug_no = request.args["bug_no"]
    result, bug_info = control.get_bug_info(current_user.role, bug_no)
    if result is False:
        return bug_info
    result, user_list = control.get_role_user(control.role_value["bug_link"])
    if result is False:
        return user_list
    return render_template("%s/BUG_Info.html" % html_dir, bug_info=bug_info, bug_status_desc=bug_status_desc, bug_no=bug_no,
                           user_role=current_user.role, current_user=current_user.account, role_desc=control.role_value,
                           user_list=user_list, url_prefix=url_prefix)


@develop_bug_view.route("/new/", methods=["POST"])
def new_bug():
    bug_title = request.form["bug_title"]
    result, bug_info = control.new_bug(current_user.account, current_user.role, bug_title)
    if result is False:
        return bug_info
    bug_no = bug_info["bug_no"]
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/str/example/", methods=["POST"])
def add_str_example(bug_no):
    str_example = request.form["bug_str_example"]
    result, example_info = control.add_bug_str_example(current_user.account, current_user.role, bug_no, str_example)
    if result is False:
        return example_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


bug_img_dir = "%s/bug/" % data_dir


@develop_bug_view.route("/<bug_no>/img/example/", methods=["POST"])
def add_img_example(bug_no):
    mine_bug_img_dir = bug_img_dir + current_user.account
    if os.path.exists(mine_bug_img_dir) is False:
        os.makedirs(mine_bug_img_dir)
    img_file = request.files["bug_img_example"]
    img_filename = secure_filename(img_file.filename)
    extend = img_filename.split(".")[-1]
    if extend not in ["png", "jpeg", "jpg", "gif"]:
        return u"不支持的图片格式"
    file_name = "%s_%s.%s" % (bug_no, datetime.now().strftime(TIME_FORMAT_STR), extend)
    save_path = "%s/%s" % (mine_bug_img_dir, file_name)
    img_file.save(save_path)
    result, example_info = control.add_bug_img_example(current_user.account, current_user.role, bug_no, file_name)
    if result is False:
        return example_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/ys/", methods=["POST"])
def add_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["POST"])
def add_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/fix/", methods=["POST"])
def add_fix_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "fix")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/cancel/", methods=["POST"])
def add_cancel_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "cancel")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/design/", methods=["POST"])
def add_design_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "design")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/ys/", methods=["DELETE"])
def del_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.delete_bug_link(bug_no, current_user.account, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["DELETE"])
def del_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.delete_bug_link(bug_no, current_user.account, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<user_name>/<img_path>/", methods=["GET"])
def get_bug_img(user_name, img_path):
    dir = "%s%s" % (bug_img_dir, user_name)
    return send_from_directory(directory=dir, filename=img_path)


