#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import Blueprint, jsonify
from flask_login import current_user

from Web import tools_url_prefix as url_prefix
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

# html_dir = "/LOG"


tools_view = Blueprint('tools_view', __name__)


@tools_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@tools_view.route("/ip/<ip_value>/", methods=["GET"])
def get_ip_info_f(ip_value):
    ip_value = int(ip_value)
    result, info = control.get_ip_info(ip_value)
    return jsonify({"status": result, "data": info})
