#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from flask import render_template, request, redirect, jsonify, g
from flask_login import current_user

from Web import param_url_prefix as url_prefix, create_blue
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Param"

develop_param_view = create_blue('develop_param_view', url_prefix=url_prefix)


@develop_param_view.route("/", methods=["GET"])
def show_param_info_func():
    return render_template("%s/Param_Info.html" % html_dir)


@develop_param_view.route("/", methods=["POST"])
def add_param_func():
    r_data = request.json
    param = r_data["param"]
    param_type = r_data["param_type"]
    del r_data["param"]
    del r_data["param_type"]
    result, info = control.add_param_format(g.user_name, g.user_role, param, param_type, **r_data)
    return jsonify({"status": result, "data": info})