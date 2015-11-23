#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from Web.views import control
from Class import TIME_FORMAT_STR

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
@login_required
def show_bug_list():
    result, bug_list = control.get_bug_list(current_user.role)
    if result is False:
        return bug_list
    return render_template("/Dev/BUG/Show_BUG.html", bug_list=bug_list, bug_status_desc=bug_status_desc,
                           user_role=current_user.role, role_value=control.user_role)


@develop_bug_view.route("/info/", methods=["GET"])
@login_required
def bug_info():
    if "bug_no" not in request.args:
        return u"请求错误"
    bug_no = request.args["bug_no"]
    result, bug_info = control.get_bug_info(current_user.role, bug_no)
    if result is False:
        return bug_info
    result, user_list = control.get_role_user(control.user_role["bug_link"])
    if result is False:
        return user_list
    return render_template("/Dev/BUG/BUG_Info.html", bug_info=bug_info, bug_status_desc=bug_status_desc,bug_no=bug_no,
                           user_role=current_user.role, current_user=current_user.account, role_value=control.user_role,
                           user_list=user_list)


@develop_bug_view.route("/new/", methods=["POST"])
@login_required
def new_bug():
    bug_title = request.form["bug_title"]
    result, bug_info = control.new_bug(current_user.account, current_user.role, bug_title)
    if result is False:
        return bug_info
    bug_no = bug_info["bug_no"]
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/str/example/", methods=["POST"])
@login_required
def add_str_example(bug_no):
    str_example = request.form["bug_str_example"]
    result, example_info = control.add_bug_str_example(current_user.account, current_user.role, bug_no, str_example)
    if result is False:
        return example_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


bug_img_dir = "static/t_images/BUG_Image/"


@develop_bug_view.route("/<bug_no>/img/example/", methods=["POST"])
@login_required
def add_img_example(bug_no):
    img_file = request.files["bug_img_example"]
    img_filename = secure_filename(img_file.filename)
    extend = img_filename.split(".")[-1]
    if extend not in ["png", "jpeg", "jpg", "gif"]:
        return u"不支持的图片格式"
    save_path = "%s%s_%s.%s" % (bug_img_dir, bug_no, datetime.now().strftime(TIME_FORMAT_STR), extend)
    img_file.save(save_path)
    result, example_info = control.add_bug_img_example(current_user.account, current_user.role, bug_no, save_path)
    if result is False:
        return example_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/ys/", methods=["POST"])
@login_required
def add_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["POST"])
@login_required
def add_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/fix/", methods=["POST"])
@login_required
def add_fix_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "fix")
    if result is False:
        return link_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/channel/", methods=["POST"])
@login_required
def add_channel_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "channel")
    if result is False:
        return link_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/design/", methods=["POST"])
@login_required
def add_design_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "design")
    if result is False:
        return link_info
    return redirect(develop_bug_view.url_prefix + "/info?bug_no=%s" % bug_no)