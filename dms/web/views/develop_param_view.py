#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import param_url_prefix as url_prefix, create_blue

from dms.utils.manager import Explorer

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Param"
rt = RenderTemplate("Param", url_prefix=url_prefix)
develop_param_view = create_blue('develop_param_view', url_prefix=url_prefix)
pf_man = Explorer.get_instance().get_object_manager("param_format")


@develop_param_view.route("/", methods=["GET"])
def show_param_info_func():
    if "X-Requested-With" in request.headers or "X-JY-FROM" in request.headers:
        result, info = pf_man.select_param_format(g.user_name, g.user_role)
        return jsonify({"status": result, "data": info})
    # if g.user_role & g.role_value["param_new"] <= 0:
    #     g.role_level = 0
    # elif g.user_role & g.role_value["param_update"] <= 0:
    #     g.role_level = 1
    # elif g.user_role & g.role_value["param_del"] <= 0:
    #     g.role_level = 2
    # else:
    g.role_level = 3
    return rt.render("Param_Info.html")


@develop_param_view.route("/", methods=["POST", "PUT"])
def add_param_func():
    r_data = request.json
    print(r_data)
    param = r_data["param"]
    del r_data["param"]
    if request.method == "POST":
        param_type = r_data["param_type"]
        del r_data["param_type"]
        result, info = pf_man.new_param_format(g.user_name, param, param_type, **r_data)
    else:
        result, info = pf_man.update_param_format(g.user_name, param, **r_data)
    return jsonify({"status": result, "data": info})


@develop_param_view.route("/query/", methods=["GET"])
def query_param():
    if "params" not in request.args:
        return jsonify({"status": True, "data": []})
    params = request.args["params"]
    exec_r, params_info = pf_man.select_mul_param_format(params)
    return jsonify({"status": exec_r, "data": params_info})
