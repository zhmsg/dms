#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import Blueprint, render_template, request, redirect
from Class.Control import ControlManager

sys.path.append('..')

__author__ = 'Zhouheng'


develop_api_view = Blueprint('develop_api_view', __name__, url_prefix="/dev/api")

control = ControlManager()

print("start success")


@develop_api_view.app_errorhandler(500)
def handle_500(e):
    print(e.args)
    return str(e.args)


@develop_api_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_api_view.route("/")
def list_api():
    result, module_list = control.get_module_list()
    if result is False:
        return module_list
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
        result, api_list = control.get_api_list(module_no)
        if result is False:
            return api_list
        current_module = None
        for module_info in module_list:
            if module_info["module_no"] == module_no:
                current_module = module_info
                break
        if current_module is None:
            return "Error"
        return render_template("/Dev/API_HELP/List_API.html",
                               module_list=module_list, api_list=api_list, current_module=current_module)
    return render_template("/Dev/API_HELP/List_API.html", module_list=module_list)


@develop_api_view.route("/new/", methods=["GET"])
def new_api_page():
    result, module_list = control.get_module_list()
    if result is False:
        return module_list
    return render_template("/Dev/API_HELP/New_API.html", module_list=module_list)


@develop_api_view.route("/new/", methods=["POST"])
def new_api_info():
    request_form = request.form
    desc = request_form["api_desc"]
    url = request_form["api_url"]
    title = request_form["api_title"]
    method = request_form["api_method"]
    module_no = int(request_form["api_module"])
    result, api_info = control.new_api_info(module_no, title, url, method, desc)
    if result is False:
        return api_info
    return redirect(develop_api_view.url_prefix + "/update/info/?api_no=%s" % api_info["api_no"])


@develop_api_view.route("/update/info/", methods=["GET"])
def update_api_other_info():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no)
    if result is False:
        return api_info
    return render_template("/Dev/API_HELP/Update_API.html", api_info=api_info, api_no=api_no)


@develop_api_view.route("/add/header/", methods=["POST"])
def add_header_param():
    request_form = request.form
    param = request_form["param"]
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    result, param_info = control.add_header_param(api_no, param, necessary, desc)
    if result is False:
        return param_info
    return "true"


@develop_api_view.route("/add/body/", methods=["POST"])
def add_body_param():
    request_form = request.form
    param = request_form["param"]
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    type = request_form["type"]
    result, param_info = control.add_body_param(api_no, param, necessary, type, desc)
    if result is False:
        return param_info
    return "true"


@develop_api_view.route("/add/input/", methods=["POST"])
def add_input_example():
    request_form = request.form
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    example = request_form["example"]
    print(request_form)
    result, input_info = control.add_input_example(api_no, example, desc)
    if result is False:
        return input_info
    return "true"


@develop_api_view.route("/add/output/", methods=["POST"])
def add_output_example():
    request_form = request.form
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    example = request_form["example"]
    result, input_info = control.add_output_example(api_no, example, desc)
    if result is False:
        return input_info
    return "true"
