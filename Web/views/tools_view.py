#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import jsonify, render_template, g

from Web import tools_url_prefix as url_prefix, create_blue
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Tools"


tools_view = create_blue('tools_view', url_prefix=url_prefix)


@tools_view.route("/", methods=["GET"])
def tools_page():
    return render_template("%s/Tools.html" % html_dir, request_ip=g.request_IP_s)


@tools_view.route("/ip/<ip_value>/", methods=["GET"])
def get_ip_info_f(ip_value):
    ip_value = int(ip_value)
    result, info = control.get_ip_info(ip_value)
    return jsonify({"status": result, "data": info})
