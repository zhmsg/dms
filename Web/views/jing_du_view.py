#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import render_template, g, request, jsonify

from Web import jingdu_url_prefix as url_prefix, create_blue, control

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