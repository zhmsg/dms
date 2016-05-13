#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from urlparse import urlparse, parse_qs
from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required, current_user
from Web import status_url_prefix, api_url_prefix
from Web.views import control


sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = status_url_prefix
html_dir = "/API_Status"

develop_status_view = Blueprint('develop_status_view', __name__)


print("start success")


@develop_status_view.before_request
@login_required
def before_request():
    pass


@develop_status_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_status_view.route("/", methods=["GET"])
def show_status_info():
    result, status_info = control.get_status(current_user.role)
    if result is False:
        return status_info
    del_status_code_url = url_prefix + "/remove/"
    fun_info_url = url_prefix + "/fun/"
    error_type_url = url_prefix + "/type/"
    return_url = api_url_prefix + ("/" if "api_no" not in request.args else "/info/?api_no=%s" % request.args["api_no"])
    search_status = "" if "status" not in request.args else request.args["status"]
    new_power = del_power = False
    if current_user.role & control.role_value["status_code_new"] > 0:
        new_power = True
    if current_user.role & control.role_value["status_code_del"] > 0:
        del_power = True
    return render_template("%s/Status_API.html" % html_dir, fun_info_url=fun_info_url, status_info=status_info,
                           error_type_url=error_type_url, return_url=return_url, search_status=search_status,
                           new_power=new_power, del_power=del_power, del_status_code_url=del_status_code_url)


@develop_status_view.route("/module/", methods=["GET"])
def new_module_page():
    return render_template("%s/Status_Module.html" % html_dir)


@develop_status_view.route("/fun/", methods=["GET"])
@login_required
def get_fun_info():
    result, fun_info = control.get_fun_info(current_user.role)
    return jsonify({"status": result, "data": fun_info})


@develop_status_view.route("/type/", methods=["GET"])
@login_required
def get_error_type():
    result, error_type = control.get_error_type(current_user.role)
    return jsonify({"status": result, "data": error_type})


@develop_status_view.route("/new/", methods=["POST"])
@login_required
def new_status():
    request_data = request.form
    service_id = int(request_data["service_id"])
    fun_id = int(request_data["fun_id"])
    type_id = int(request_data["type_id"])
    error_id = int(request_data["error_id"])
    error_desc = request_data["error_desc"]
    result, new_info = control.new_api_status(current_user.account, current_user.role, service_id, fun_id, type_id,
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
    return redirect(redirect_url)


@develop_status_view.route("/remove/", methods=["GET"])
@login_required
def remove_status_code():
    status_code = int(request.args["status_code"])
    result, info = control.delete_api_status(current_user.account, current_user.role, status_code)
    if result is False:
        return info
    return redirect("%s/?status=%s" % (url_prefix, status_code))