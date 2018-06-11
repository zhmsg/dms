#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import jsonify, render_template, g, request

from Class.IP import IPManager

from Web import tools_url_prefix as url_prefix, create_blue
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Tools"


tools_view = create_blue('tools_view', url_prefix=url_prefix)
ip_man = IPManager()


@tools_view.route("/", methods=["GET"])
def tools_page():
    ip_group_url = url_prefix + "/ip/group/"
    return render_template("%s/Tools.html" % html_dir, request_ip=g.request_IP_s, ip_group_url=ip_group_url)


@tools_view.route("/ip/<int:ip_value>/", methods=["GET"])
def get_ip_info_f(ip_value):
    ip_value = int(ip_value)
    result, info = control.get_ip_info(ip_value)
    return jsonify({"status": result, "data": info})


@tools_view.route("/ip/group/", methods=["GET"])
def get_ip_group():
    db_items = ip_man.select(g_name=request.args.get("g_name"))
    return jsonify({"status": True, "data": db_items})


@tools_view.route("/ip/group/", methods=["POST"])
def add_ip_group():
    data = request.json
    g_name = data["g_name"]
    ip_value = data["ip_value"]
    exec_r = ip_man.insert_one(g_name, ip_value)
    return jsonify({"status": True, "data": "success"})