#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from urlparse import urlparse, parse_qs
from flask import render_template, request, redirect, jsonify
from flask_login import current_user
from Web import status_url_prefix, api_url_prefix, create_blue
from Web import control


sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = status_url_prefix
html_dir = "/API_Status"

develop_status_view = create_blue('develop_status_view', url_prefix=url_prefix)


@develop_status_view.route("/", methods=["GET"])
def show_status_info_page():
    del_status_code_url = url_prefix + "/remove/"
    fun_info_url = url_prefix + "/fun/"
    error_type_url = url_prefix + "/type/"
    url_code = url_prefix + "/code/"
    return_url = api_url_prefix + ("/" if "api_no" not in request.args else "/info/?api_no=%s" % request.args["api_no"])
    search_status = "" if "status" not in request.args else request.args["status"]
    new_power = del_power = new_module_power = False
    if current_user.role & control.role_value["status_code_new"] > 0:
        new_power = True
    if current_user.role & control.role_value["status_code_del"] > 0:
        del_power = True
    if current_user.role & control.role_value["status_code_module"] > 0:
        new_module_power = True

    if new_power is False:
        return redirect(url_prefix + "/q/")
    return render_template("%s/Status_API.html" % html_dir, fun_info_url=fun_info_url, error_type_url=error_type_url,
                           return_url=return_url, search_status=search_status,
                           new_power=new_power, del_power=del_power, new_module_power=new_module_power,
                           del_status_code_url=del_status_code_url, url_code=url_code)


@develop_status_view.route("/q/", methods=["GET"])
def query_status_page():
    if "status" in request.args:
        result, status_info = control.get_status(current_user.role, status_code=request.args["status"])
        return jsonify({"status": result, "data": {"items": status_info, "q": request.args["status"]}})
    del_status_code_url = url_prefix + "/remove/"
    fun_info_url = url_prefix + "/fun/"
    error_type_url = url_prefix + "/type/"
    return_url = api_url_prefix + ("/" if "api_no" not in request.args else "/info/?api_no=%s" % request.args["api_no"])
    search_status = "" if "status" not in request.args else request.args["status"]
    new_power = del_power = new_module_power = False
    if current_user.role & control.role_value["status_code_new"] > 0:
        new_power = True
    if current_user.role & control.role_value["status_code_del"] > 0:
        del_power = True
    if current_user.role & control.role_value["status_code_module"] > 0:
        new_module_power = True
    return render_template("%s/Status_Info.html" % html_dir, fun_info_url=fun_info_url,
                           error_type_url=error_type_url, return_url=return_url, search_status=search_status,
                           new_power=new_power, del_power=del_power, new_module_power=new_module_power,
                           del_status_code_url=del_status_code_url)


@develop_status_view.route("/module/", methods=["GET"])
def new_module_page():
    return_url = url_prefix
    fun_info_url = url_prefix + "/fun/"
    error_type_url = url_prefix + "/type/"
    return render_template("%s/Status_Module.html" % html_dir, return_url=return_url, fun_info_url=fun_info_url,
                           error_type_url=error_type_url)


@develop_status_view.route("/module/", methods=["POST"])
def new_module():
    request_data = request.json
    module_title = request_data["module_title"]
    module_desc = request_data["module_desc"]
    result, info = control.new_service_module(current_user.user_name, current_user.role, module_title, module_desc)

    return jsonify({"status": result, "data": info})


@develop_status_view.route("/fun/", methods=["GET"])
def get_fun_info():
    result, fun_info = control.get_fun_info(current_user.role)
    return jsonify({"status": result, "data": fun_info})


@develop_status_view.route("/fun/", methods=["POST"])
def new_fun_info():
    request_data = request.json
    service_id = request_data["service_id"]
    sub_module_title = request_data["sub_module_title"]
    sub_module_desc = request_data["sub_module_desc"]
    result, info = control.new_function_module(current_user.user_name, current_user.role, service_id,
                                               sub_module_title, sub_module_desc)
    return jsonify({"status": result, "data": info})


@develop_status_view.route("/type/", methods=["GET"])
def get_error_type():
    result, error_type = control.get_error_type(current_user.role)
    return jsonify({"status": result, "data": error_type})


@develop_status_view.route("/code/", methods=["GET"])
def get_code_info():
    if "status" in request.args:
        result, status_info = control.get_status(current_user.role, status_code=request.args["status"])
    else:
        result, status_info = control.get_status(current_user.role)
    return jsonify({"status": result, "data": status_info})


@develop_status_view.route("/code/", methods=["POST"])
def new_status():
    request_data = request.json
    service_id = int(request_data["service_id"])
    fun_id = int(request_data["fun_id"])
    type_id = int(request_data["type_id"])
    error_id = int(request_data["error_id"])
    error_desc = request_data["error_desc"]
    result, new_info = control.new_api_status(current_user.user_name, current_user.role, service_id, fun_id, type_id,
                                              error_id, error_desc)
    if result is False:
        return new_info
    redirect_url = urlparse(request.headers["Referer"])
    uq = parse_qs(redirect_url.query)
    uq["status"] = [new_info]
    param_list = []
    for key in uq:
        param_list.append("%s=%s" % (key, uq[key][0]))
    redirect_url = redirect_url.path + "?" + "&".join(param_list)
    return jsonify({"status": True, "data": "", "location": redirect_url})


@develop_status_view.route("/remove/", methods=["GET"])
def remove_status_code():
    status_code = int(request.args["status_code"])
    result, info = control.delete_api_status(current_user.user_name, current_user.role, status_code)
    if result is False:
        return info
    return redirect("%s/?status=%s" % (url_prefix, status_code))


@develop_status_view.route("/code/", methods=["DELETE"])
def remove_status_code_d():
    status_code = int(request.json["status_code"])
    result, info = control.delete_api_status(current_user.user_name, current_user.role, status_code)
    if result is False:
        return info
    return jsonify({"status": True, "data": request.json["status_code"]})


@develop_status_view.route("/mul/", methods=["GET"])
def new_mul_status_page():
    return_url = url_prefix
    fun_info_url = url_prefix + "/fun/"
    error_type_url = url_prefix + "/type/"
    del_status_code_url = url_prefix + "/code/"
    return render_template("%s/New_Mul_Status.html" % html_dir, return_url=return_url, fun_info_url=fun_info_url,
                           error_type_url=error_type_url, del_status_code_url=del_status_code_url)


@develop_status_view.route("/mul/", methods=["POST"])
def new_mul_status():
    request_data = request.json
    service_id = int(request_data["service_id"])
    fun_id = int(request_data["fun_id"])
    error_info = request_data["error_info"]
    result, info = control.new_mul_api_status(current_user.user_name, current_user.role, service_id, fun_id, error_info)
    return jsonify({"status": result, "data": info})
