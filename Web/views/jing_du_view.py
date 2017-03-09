#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from flask import render_template, g, request, jsonify

from Web import jingdu_url_prefix as url_prefix, create_blue, control, sx_variant, check_variant

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/JingDu"

jing_du_view = create_blue('jing_du_view', url_prefix=url_prefix, special_protocol=True)


@jing_du_view.route("/", methods=["GET"])
def index():
    return render_template("%s/Index.html" % html_dir)


@jing_du_view.route("/project/", methods=["GET"])
def get_project_info():
    if "project_no" in request.args:
        project_no = int(request.args["project_no"])
    else:
        project_no = None
    exec_r, mul_p_info = control.get_project_info(g.user_name, g.user_role, project_no)
    return jsonify({"status": exec_r, "data": mul_p_info})


@jing_du_view.route("/project/user/", methods=["GET"])
def get_project_user():
    project_no = account = None
    if "project_no" in request.args:
        project_no = int(request.args["project_no"])
    elif "account" in request.args:
        account = request.args["account"]
    else:
        return jsonify({"status": False, "data": "无效的请求"})
    exec_r, mul_pu_info = control.get_project_user(g.user_name, g.user_role, project_no, account)
    return jsonify({"status": exec_r, "data": mul_pu_info})


@jing_du_view.route("/sample/", methods=["GET"])
def get_sys_sample():
    if "sample_no" in request.args:
        sample_no = int(request.args["sample_no"])
    else:
        sample_no = None
    exec_r, mul_s_info = control.get_sys_sample(g.user_name, g.user_role, sample_no)
    return jsonify({"status": exec_r, "data": mul_s_info})


@jing_du_view.route("/sample/info/", methods=["GET"])
def get_sample_info():
    sample_no = None
    if "sample_no" in request.args:
        sample_no = int(request.args["sample_no"])
    else:
        return jsonify({"status": False, "data": "无效的请求"})
    exec_r, mul_si_info = control.get_sample_info(g.user_name, g.user_role, sample_no)
    return jsonify({"status": exec_r, "data": mul_si_info})


@jing_du_view.route("/sample/user/", methods=["GET"])
def get_sample_user():
    sample_no = account = None
    if "sample_no" in request.args:
        sample_no = int(request.args["sample_no"])
    elif "account" in request.args:
        account = request.args["account"]
    else:
        return jsonify({"status": False, "data": "无效的请求"})
    exec_r, mul_su_info = control.get_sample_user(g.user_name, g.user_role, sample_no, account)
    return jsonify({"status": exec_r, "data": mul_su_info})


@jing_du_view.route("/sample/variant/", methods=["GET"])
def check_sample_variant():
    if "sample_no" in request.args:
        sample_no = int(request.args["sample_no"])
    else:
        return jsonify({"status": False, "data": "无效的请求"})
    r_data = dict(sample_no=sample_no)
    if check_variant[0] is True:
        r_data["message"] = "正忙"
        return jsonify({"status": True, "data": r_data})
    check_variant[0] = True
    try:
        resp = requests.get("%s/head/%s/" % (sx_variant, sample_no))
        if resp.status_code != 200:
            r_data["message"] = "请求%s" % resp.status_code
            r_data["detail"] = resp.status_code
        else:
            r_data["detail"] = resp.text
            res = resp.json()
            if "status" not in res:
                r_data["message"] = "生信格式不正确"
            elif res["status"].lower() != "success":
                r_data["message"] = "生信格式不正确"
            elif "vars" not in res:
                r_data["message"] = "生信格式不正确"
            else:
                r_data["message"] = "正常"
                r_data["detail"] = "检测通过"
    except Exception as ce:
        print(ce)
        r_data["message"] = "请求失败"
        r_data["detail"] = str(ce)
    check_variant[0] = False
    return jsonify({"status": True, "data": r_data})


@jing_du_view.route("/task/", methods=["GET"])
def query_task():
    kwargs = dict()
    keys = ["started_stamp", "app_id", "s_status", "e_status"]
    for k in keys:
        if k in request.args:
            kwargs[k] = request.args[k]
    kwargs["order_by"] = ["started_stamp"]
    kwargs["order_desc"] = True
    exec_r, task_data = control.query_task(g.user_name, g.user_role, **kwargs)
    return jsonify({"status": exec_r, "data": task_data})


@jing_du_view.route("/app/", methods=["GET"])
def get_app_list():
    exec_r, app_info = control.get_app_list(g.user_name, g.user_role)
    return jsonify({"status": exec_r, "data": app_info})
