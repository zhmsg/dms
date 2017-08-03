#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import dyups_url_prefix as url_prefix, create_blue
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'

rt = RenderTemplate("Dyups", url_prefix=url_prefix)
develop_dyups_view = create_blue('develop_dyups_view', url_prefix=url_prefix)


@develop_dyups_view.route("/", methods=["GET"])
def index_page():
    webcluster_role = control.role_value["dyups_web"]
    apicluster_role = control.role_value["dyups_api"]
    op_server_url = url_prefix + "/server/"
    op_upstream_url = url_prefix + "/upstream/"
    return rt.render("Index.html", webcluster_role=webcluster_role, apicluster_role=apicluster_role,
                     op_server_url=op_server_url, op_upstream_url=op_upstream_url)


@develop_dyups_view.route("/<upstream_name>/", methods=["GET"])
def web_upstream(upstream_name):
    exec_r, data = control.get_server_list(g.user_name, g.user_role, upstream_name)
    r_data = {"name": upstream_name, "data": data}
    return jsonify({"status": exec_r, "data": r_data})


@develop_dyups_view.route("/upstream/", methods=["POST", "DELETE"])
def remove_upstream():
    request_data = request.json
    server_ip = request_data["server_ip"]
    server_port = int(request_data["server_port"])
    upstream_name = request_data["upstream_name"]
    if request.method == "DELETE":
        exec_r, data = control.remove_upstream(g.user_name, g.user_role, upstream_name, server_ip, server_port)
    else:
        exec_r, data = control.add_upstream(g.user_name, g.user_role, upstream_name, server_ip, server_port)
    return jsonify({"status": exec_r, "data": data})


@develop_dyups_view.route("/server/", methods=["POST", "DELETE"])
def op_server_nodes():
    request_data = request.json
    server_ip = request_data["server_ip"]
    server_port = int(request_data["server_port"])
    upstream_name = request_data["upstream_name"]
    if request.method == "POST":
        exec_r, data = control.add_server_node(g.user_name, g.user_role, upstream_name, server_ip, server_port)
    else:
        exec_r, data = control.delete_server_node(g.user_name, g.user_role, upstream_name, server_ip, server_port)
    return jsonify({"status": exec_r, "data": data})
