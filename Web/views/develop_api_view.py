#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
from functools import wraps
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import api_url_prefix, create_blue, test_url_prefix, status_url_prefix, param_url_prefix
from Web import control


sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = api_url_prefix

rt = RenderTemplate("API_HELP", url_prefix=url_prefix)


develop_api_view = create_blue('develop_api_view', url_prefix=url_prefix)


def referer_api_no(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Referer" not in request.headers:
            return jsonify({"status": False, "data": "Bad Request"})
        g.ref_url = request.headers["Referer"]
        find_result = re.findall("api_no=([a-z\d]{32})", g.ref_url)
        if len(find_result) > 0:
            g.api_no = find_result[0]
        elif "api_no" in request.args:
            g.api_no = request.args["api_no"]
        else:
            return jsonify({"status": False, "data": "Bad Request."})
        return f(*args, **kwargs)
    return decorated_function


def referer_module_no(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Referer" not in request.headers:
            return jsonify({"status": False, "data": "Bad Request"})
        g.ref_url = request.headers["Referer"]
        find_result = re.findall("module_no=(\d{1,5})", g.ref_url)
        if len(find_result) > 0:
            g.module_no = find_result[0]
        elif "module_no" in request.args:
            g.module_no = request.args["module_no"]
        else:
            return jsonify({"status": False, "data": "Bad Request."})
        return f(*args, **kwargs)

    return decorated_function


@develop_api_view.route("/", methods=["GET"])
def list_api():
    test_module_url = test_url_prefix + "/batch/"
    test_env_url = test_url_prefix + "/env/"
    module_url = url_prefix + "/module/"
    return rt.render("List_API.html", test_module_url=test_module_url, test_env_url=test_env_url,
                     module_url=module_url)


@develop_api_view.route("/module/", methods=["GET"])
def get_module_api():
    if "module_no" not in request.args:
        result, part_module = control.get_part_api(g.user_name, g.user_role)
        return jsonify({"status": result, "data": part_module})
    module_no = int(request.args["module_no"])
    result, module_data = control.get_api_list(module_no, g.user_role)
    return jsonify({"status": result, "data": module_data})


@develop_api_view.route("/module/", methods=["POST", "PUT"])
def new_api_module():
    request_data = request.json
    module_name = request_data["module_name"]
    module_prefix = request_data["module_prefix"]
    module_desc = request_data["module_desc"]
    module_part = int(request_data["module_part"])
    module_env = request_data["module_env"]
    if request.method == "POST":
        result, message = control.new_api_module(g.user_role, module_name, module_prefix, module_desc, module_part,
                                                 module_env)
    else:
        module_no = request_data["module_no"]
        result, message = control.update_api_module(g.user_role, module_no, module_name, module_prefix, module_desc,
                                                    module_part, module_env)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/module/care/", methods=["POST", "DELETE"])
@referer_module_no
def add_module_care():
    module_no = int(g.module_no)
    if request.method == "POST":
        result, care_info = control.add_module_care(g.user_name, g.user_role, module_no)
    else:
        result, care_info = control.delete_module_care(g.user_name, module_no)
    return jsonify({"status": result, "data": care_info})


@develop_api_view.route("/info/", methods=["GET"])
def show_api():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"][:32]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no, g.user_role)
    if result is False:
        return api_info
    if g.accept_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": True, "data": {"api_info": api_info}})
    return_url = url_prefix + "/info/?api_no=%s" % api_no
    if "update" in request.args:
        update_stage_url = url_prefix + "/stage/"
        return rt.render("Update_API.html", api_no=api_no, return_url=return_url, update_stage_url=update_stage_url)
    test_url = url_prefix + "/test/?api_no=%s" % api_no
    batch_test_url = url_prefix + "/test/batch/?api_no=%s" % api_no
    status_url = status_url_prefix
    param_url = param_url_prefix + "/query/"
    return_url = url_prefix + "/?module_no=%s" % api_info["basic_info"]["module_no"]
    return rt.render("Show_API.html", api_no=api_no, return_url=return_url, test_url=test_url, status_url=status_url,
                     batch_test_url=batch_test_url, param_url=param_url)


@develop_api_view.route("/basic/", methods=["GET"])
def new_api_page():
    result, part_module = control.get_part_api(g.user_name, g.user_role)
    if result is False:
        return part_module
    if "api_no" in request.args:
        api_no = request.args["api_no"]
        if len(api_no) != 32:
            return "Bad api_no"
        api_info_url = url_prefix + "/info/?api_no=%s" % api_no
        return rt.render("New_API.html", part_module=part_module, api_info_url=api_info_url)

    return rt.render("New_API.html", part_module=part_module)


@develop_api_view.route("/basic/", methods=["POST", "PUT"])
def new_update_api_info():
    request_data = request.json
    api_module = request_data["api_module"]
    desc = request_data["api_desc"]
    url = request_data["api_path"]
    title = request_data["api_title"]
    method = request_data["api_method"]
    module_no = int(api_module)
    if request.method == "PUT":
        api_no = request_data["api_no"]
        r, m = control.update_api_info(role=g.user_role, api_no=api_no, desc=desc, method=method, path=url,
                                       module_no=module_no, title=title)
        if r is False:
            return jsonify({"status": False, "data": m})
    else:
        r, api_info = control.new_api_info(module_no, title, url, method, desc, g.user_name, g.user_role)
        if r is False:
            return jsonify({"status": False, "data": api_info})
        api_no = api_info["api_no"]
    return jsonify({"status": True, "location": "%s/info/?api_no=%s&update=" % (url_prefix, api_no), "data": "success"})


@develop_api_view.route("/basic/", methods=["DELETE"])
@referer_api_no
def delete_api():
    result, data = control.delete_api(g.api_no, g.user_name)
    if result is False:
        return jsonify({"status": False, "data": data})
    return jsonify({"status": True, "location": url_prefix + "/", "data": "success"})


@develop_api_view.route("/stage/", methods=["PUT"])
@referer_api_no
def update_api_status_func():
    api_no = g.api_no
    stage = request.json["stage"]
    result, info = control.set_api_status(g.user_name, g.user_role, api_no, stage)
    if result is False:
        return jsonify({"status": False, "data": info})
    return jsonify({"status": True, "location": g.ref_url, "data": "success"})


@develop_api_view.route("/header/", methods=["POST"])
@referer_api_no
def add_header_param():
    request_data = request.json
    param = request_data["name"]
    api_no = g.api_no
    desc = request_data["desc"]
    necessary = int(request_data["necessary"])
    result, param_info = control.add_header_param(g.user_name, g.user_role, api_no, param, necessary, desc)
    return jsonify({"status": result, "data": param_info})


@develop_api_view.route("/header/", methods=["PUT"])
@referer_api_no
def update_api_predefine_header():
    api_no = g.api_no
    request_data = request.json
    param = request_data["param"]
    update_type = request_data["update_type"]
    param_type = "header"
    if update_type == "delete":
        result, message = control.delete_predefine_param(g.user_role, api_no, param)
    else:
        result, message = control.add_predefine_header(g.user_name, api_no, param, param_type, g.user_role)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/header/", methods=["DELETE"])
@referer_api_no
def delete_header():
    request_data = request.json
    api_no = g.api_no
    if "param" in request_data:
        result, data = control.delete_header(g.user_role, api_no, request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/body/", methods=["GET"])
@referer_api_no
def update_api_body_page():
    api_no = g.api_no
    body_url = url_prefix + "/body/"
    return rt.render("Update_API_Param.html", api_no=api_no, body_url=body_url)


@develop_api_view.route("/body/", methods=["POST"])
@referer_api_no
def add_body_param():
    request_data = request.json
    param = request_data["name"]
    api_no = g.api_no
    param_desc = request_data["desc"]
    necessary = int(request_data["necessary"])
    param_type = request_data["type"]
    status = int(request_data.get("status", "1"))
    result, param_info = control.add_body_param(g.user_name, api_no, param, necessary, param_type, param_desc,
                                                status, g.user_role)
    return jsonify({"status": result, "data": param_info})


@develop_api_view.route("/body/", methods=["PUT"])
@referer_api_no
def update_api_predefine_body():
    api_no = g.api_no
    request_data = request.json
    param = request_data["param"]
    update_type = request_data["update_type"]
    param_type = "body"
    if update_type == "delete":
        result, message = control.delete_predefine_param(g.user_role, api_no, param)
    else:
        result, message = control.add_predefine_header(g.user_name, api_no, param, param_type, g.user_role)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/body/", methods=["DELETE"])
@referer_api_no
def delete_body():
    request_data = request.json
    api_no = g.api_no
    if "param" in request_data:
        result, data = control.delete_body(g.user_role, api_no, request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/example/", methods=["POST"])
@referer_api_no
def add_api_example():
    request_form = request.json
    api_no = g.api_no
    example_type = int(request_form["example_type"])
    desc = request_form["desc"]
    content = request_form["content"]
    result, data = control.add_api_example(g.user_name, g.user_role, api_no, example_type, desc, content)
    return jsonify({"status": result, "data": data})


@develop_api_view.route("/example/", methods=["DELETE"])
@referer_api_no
def delete_api_example():
    request_data = request.json
    api_no = g.api_no
    example_no = request_data["example_no"]
    result, data = control.delete_api_example(g.user_role, example_no)
    return jsonify({"status": result, "data": data})


@develop_api_view.route("/care/", methods=["POST", "DELETE"])
def add_care():
    request_data = request.json
    api_no = request_data["api_no"]
    if request.method == "POST":
        result, care_info = control.add_care(api_no, g.user_name, g.user_role)
    else:
        result, care_info = control.delete_care(api_no, g.user_name)
    return jsonify({"status": result, "data": care_info})
