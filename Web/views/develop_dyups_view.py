#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from datetime import datetime, timedelta
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import dyups_url_prefix as url_prefix, create_blue, user_blacklist, dms_scheduler, current_env, dms_job
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'

rt = RenderTemplate("Dyups", url_prefix=url_prefix)
develop_dyups_view = create_blue('develop_dyups_view', url_prefix=url_prefix)


@develop_dyups_view.route("/", methods=["GET"])
def index_page():
    return rt.render("Index.html")


@develop_dyups_view.route("/web/", methods=["GET"])
def web_upstream():
    upstream_name = "webcluster"
    exec_r, data = control.get_upstream(g.user_name, g.user_role, upstream_name)
    r_data = {"name": upstream_name, "data": data}
    return jsonify({"status": exec_r, "data": r_data})


@develop_dyups_view.route("/api/", methods=["GET"])
def api_upstream():
    upstream_name = "apicluster"
    exec_r, data = control.get_upstream(g.user_name, g.user_role, upstream_name)
    r_data = {"name": upstream_name, "data": data}
    return jsonify({"status": exec_r, "data": r_data})


@develop_dyups_view.route("/web/", methods=["POST"])
def add_web_upstream():
    request_data = request.json
    server_ip = request_data["server_ip"]
    server_port = int(request_data.get("server_port", 80))
    exec_r, data = control.add_web_upstream(g.user_name, g.user_role, server_ip, server_port)
    return jsonify({"status": exec_r, "data": data})


@develop_dyups_view.route("/api/", methods=["POST"])
def add_api_upstream():
    request_data = request.json
    server_ip = request_data["server_ip"]
    server_port = int(request_data.get("server_port", 80))
    exec_r, data = control.add_api_upstream(g.user_name, g.user_role, server_ip, server_port)
    return jsonify({"status": exec_r, "data": data})
