#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import random
import os
from datetime import datetime
from time import sleep
from flask import Blueprint, render_template, request, redirect,jsonify, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from threading import Thread

from Web.views import control
from Class import TIME_FORMAT_STR

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = "/dev/bug"

develop_bug_view = Blueprint('develop_bug_view', __name__, url_prefix=url_prefix)

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
                           user_role=current_user.role, role_value=control.user_role, url_prefix=url_prefix)


@develop_bug_view.route("/statistic/", methods=["GET"])
@login_required
def get_statistic():
    result, sta_info = control.get_bug_statistic(current_user.role)
    return jsonify({"status": result, "data": sta_info})


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
    return render_template("/Dev/BUG/BUG_Info.html", bug_info=bug_info, bug_status_desc=bug_status_desc, bug_no=bug_no,
                           user_role=current_user.role, current_user=current_user.account, role_value=control.user_role,
                           user_list=user_list, url_prefix=url_prefix)


@develop_bug_view.route("/new/", methods=["POST"])
@login_required
def new_bug():
    bug_title = request.form["bug_title"]
    result, bug_info = control.new_bug(current_user.account, current_user.role, bug_title)
    if result is False:
        return bug_info
    bug_no = bug_info["bug_no"]
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/str/example/", methods=["POST"])
@login_required
def add_str_example(bug_no):
    str_example = request.form["bug_str_example"]
    result, example_info = control.add_bug_str_example(current_user.account, current_user.role, bug_no, str_example)
    if result is False:
        return example_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


# bug_img_dir = "static/t_images/BUG_Image/"
bug_img_dir = "/data/dms/bug/"


@develop_bug_view.route("/<bug_no>/img/example/", methods=["POST"])
@login_required
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
@login_required
def add_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["POST"])
@login_required
def add_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/fix/", methods=["POST"])
@login_required
def add_fix_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "fix")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/cancel/", methods=["POST"])
@login_required
def add_cancel_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "cancel")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/design/", methods=["POST"])
@login_required
def add_design_user(bug_no):
    result, link_info = control.add_bug_link(bug_no, current_user.account, current_user.role, current_user.account, "design")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/ys/", methods=["DELETE"])
@login_required
def del_ys_user(bug_no):
    ys_user = request.form["ys_user"]
    result, link_info = control.delete_bug_link(bug_no, current_user.account, current_user.role, ys_user, "ys")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<bug_no>/owner/", methods=["DELETE"])
@login_required
def del_own_user(bug_no):
    bug_owner = request.form["owner"]
    result, link_info = control.delete_bug_link(bug_no, current_user.account, current_user.role, bug_owner, "owner")
    if result is False:
        return link_info
    return redirect(url_prefix + "/info?bug_no=%s" % bug_no)


@develop_bug_view.route("/<user_name>/<img_path>/", methods=["GET"])
@login_required
def get_bug_img(user_name, img_path):
    dir = "%s%s" % (bug_img_dir, user_name)
    return send_from_directory(directory=dir, filename=img_path)


@develop_bug_view.route("/upload/", methods=["POST"])
def upload_test():
    try:
        mine_bug_img_dir = bug_img_dir + "upload"
        if os.path.exists(mine_bug_img_dir) is False:
            os.makedirs(mine_bug_img_dir)
        save_paths = []
        for key, file in request.files.items():
            origin_filename = secure_filename(file.filename)
            file_name = "%s_%s_%s" % (datetime.now().strftime(TIME_FORMAT_STR), random.randint(10000, 99999), origin_filename)
            save_path = "%s/%s" % (mine_bug_img_dir, file_name)
            file.save(save_path)
            if os.path.exists(save_path) is False:
                return json.dumps({"result": False, "data": "File not exist. file path is %s" % save_path})
            save_paths.append(save_path)
        return json.dumps({"result": True, "data": save_paths})

    except Exception as e:
        error_mesage = str(e.args)
        return json.dumps({"result": False, "data": error_mesage})


@develop_bug_view.route("/testUpload/", methods=["GET"])
def test_upload():
    return render_template("testUpload.html")


@develop_bug_view.route("/thread/", methods=["GET"])
def test_thread():
    begin_time = datetime.now()
    print("%s enter view" % begin_time)
    t = Thread(target=run_Thread)
    t.setDaemon(True)
    t.start()
    end_time = datetime.now()
    print("%s out view" % end_time)
    run_time = (end_time - begin_time).total_seconds()
    return str(run_time)


def run_Thread():
    print("%s enter thread" % datetime.now())
    sleep(30)
    print("%s out thread" % datetime.now())

