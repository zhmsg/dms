#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import re
from urlparse import urlparse, parse_qs
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from Web import api_url_prefix
from Web.views import control


sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = api_url_prefix
html_dir = "/API_HELP"

develop_api_view = Blueprint('develop_api_view', __name__)


print("start success")


@develop_api_view.app_errorhandler(500)
def handle_500(e):
    print(e.args)
    return str(e.args)


@develop_api_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_api_view.route("/")
@login_required
def list_api():
    result, module_list = control.get_module_list(current_user.role)
    if result is False:
        return module_list
    if current_user.role & control.role_value["api_module_new"] == control.role_value["api_module_new"]:
        new_power = True
    else:
        new_power = False
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
        result, module_data = control.get_api_list(module_no, current_user.role)
        if result is False:
            return module_data
        current_module = None
        for key, module_part in module_list.items():
            for module_info in module_part:
                if module_info["module_no"] == module_no:
                    current_module = module_info
                    break
        if current_module is None:
            return "Error"
        if "update" in request.args and request.args["update"] == "true" and new_power is True:
            update_module = True
        else:
            update_module = False
        my_care = None
        for item in module_data["care_info"]:
            if item["user_name"] == current_user.account:
                my_care = item
                module_data["care_info"].remove(item)
                break
        return render_template("%s/List_API.html" % html_dir, module_list=module_list, api_list=module_data["api_list"],
                               current_module=current_module, url_prefix=url_prefix, update_module=update_module,
                               new_power=new_power, my_care=my_care, care_info=module_data["care_info"])
    return render_template("%s/List_API.html" % html_dir, module_list=module_list, url_prefix=url_prefix,
                           new_module=True, new_power=new_power)


@develop_api_view.route("/module/", methods=["POST"])
@login_required
def new_api_module_page():
    module_name = request.form["module_name"]
    module_prefix = request.form["module_prefix"]
    module_desc = request.form["module_desc"]
    if "Referer" in request.headers:
        redirect_url = request.headers["Referer"]
    else:
        redirect_url = url_prefix
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
        result, message = control.update_api_module(current_user.role, module_no, module_name, module_prefix, module_desc)
        redirect_url = "%s?module_no=%s" % (url_prefix, module_no)
    else:
        result, message = control.new_api_module(current_user.role, module_name, module_prefix, module_desc)
    if result is False:
        return message
    return redirect(redirect_url)


@develop_api_view.route("/module/care/", methods=["POST", "DELETE"])
@login_required
def add_module_care():
    request_form = request.form
    module_no = int(request_form["module_no"])
    if request.method == "POST":
        result, care_info = control.add_module_care(current_user.account, current_user.role, module_no)
    else:
        result, care_info = control.delete_module_care(current_user.account, module_no)
    return json.dumps({"status": result, "data": care_info})


@develop_api_view.route("/info/", methods=["GET"])
@login_required
def show_api():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no, current_user.role)
    if result is False:
        return api_info
    return_url = url_prefix + "/?module_no=%s" % api_info["basic_info"]["module_no"]
    update_url = None
    if current_user.role & 16 > 0:
        update_url = url_prefix + "/update/info/?api_no=%s" % api_no
    test_url = url_prefix + "/test/?api_no=%s" % api_no
    status_url = url_prefix + "/status/"
    my_care = None
    for item in api_info["care_info"]:
        if item["user_name"] == current_user.account:
            my_care = item
            api_info["care_info"].remove(item)
            break
    return render_template("%s/Show_API.html" % html_dir, api_info=api_info, api_no=api_no, return_url=return_url,
                           update_url=update_url, my_care=my_care, test_url=test_url, url_prefix=url_prefix,
                           status_url=status_url, api_status_desc=control.api_help.api_status_desc)


@develop_api_view.route("/new/", methods=["GET"])
@login_required
def new_api_page():
    result, module_list = control.get_module_list(current_user.role)
    if result is False:
        return module_list
    module_no = 1
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
    return render_template("%s/New_API.html" % html_dir, module_list=module_list, url_prefix=url_prefix,
                           module_no=module_no)


@develop_api_view.route("/new/", methods=["POST"])
@login_required
def new_api_info():
    request_form = request.form
    api_module = request_form["api_module"]
    if api_module == "":
        return "请选择API所属模块"
    desc = request_form["api_desc"]
    url = request_form["api_url"]
    title = request_form["api_title"]
    method = request_form["api_method"]
    module_no = int(api_module)
    result, api_info = control.new_api_info(module_no, title, url, method, desc, current_user.account, current_user.role)
    if result is False:
        return api_info
    return redirect(url_prefix + "/update/info/?api_no=%s" % api_info["api_no"])


@develop_api_view.route("/update/", methods=["GET"])
@login_required
def update_api_info_page():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, module_list = control.get_module_list(current_user.role)
    if result is False:
        return module_list
    result, api_info = control.get_api_info(api_no, current_user.role)
    return_url = url_prefix + "/info/?api_no=%s" % api_no
    if result is False:
        return api_info
    module_no = api_info["basic_info"]["module_no"]
    return render_template("%s/New_API.html" % html_dir, module_list=module_list, url_prefix=url_prefix,
                           module_no=module_no, api_info=api_info, return_url=return_url)


@develop_api_view.route("/update/", methods=["POST"])
@login_required
def update_api_info():
    request_form = request.form
    api_module = request_form["api_module"]
    api_no = request_form["api_no"]
    desc = request_form["api_desc"]
    url = request_form["api_url"]
    title = request_form["api_title"]
    method = request_form["api_method"]
    module_no = int(api_module)
    result, message = control.update_api_info(role=current_user.role, api_no=api_no, desc=desc, method=method,
                                              path=url, module_no=module_no, title=title)
    if result is False:
        return message
    return redirect("%s/info/?api_no=%s" % (url_prefix, api_no))


@develop_api_view.route("/update/info/", methods=["GET"])
@login_required
def update_api_other_info():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no, current_user.role)
    return_url = url_prefix + "/info/?api_no=%s" % api_no
    if result is False:
        return api_info
    return render_template("%s/Update_API.html" % html_dir, api_info=api_info, api_no=api_no, return_url=return_url,
                           url_prefix=url_prefix, api_status_desc=control.api_help.api_status_desc)


@develop_api_view.route("/update/completed/", methods=["GET"])
def set_api_completed():
    if "Referer" not in request.headers:
        return jsonify({"status": False, "data": "Bad Request"})
    ref_url = request.headers["Referer"]
    find_result = re.findall("api_no=([a-z\d]{32})", ref_url)
    if len(find_result) < 0:
        return jsonify({"status": False, "data": "Bad Request."})
    api_no = find_result[0]
    result, info = control.set_api_completed(current_user.account, current_user.role, api_no)
    if result is False:
        return info
    return redirect(ref_url)


@develop_api_view.route("/update/modify/", methods=["GET"])
def set_api_modify():
    if "Referer" not in request.headers:
        return jsonify({"status": False, "data": "Bad Request"})
    ref_url = request.headers["Referer"]
    find_result = re.findall("api_no=([a-z\d]{32})", ref_url)
    if len(find_result) < 0:
        return jsonify({"status": False, "data": "Bad Request."})
    api_no = find_result[0]
    result, info = control.set_api_modify(current_user.account, current_user.role, api_no)
    if result is False:
        return info
    return redirect(ref_url)


@develop_api_view.route("/add/header/", methods=["POST"])
@login_required
def add_header_param():
    request_form = request.form
    param = request_form["param"]
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    result, param_info = control.add_header_param(current_user.account, api_no, param, necessary, desc, current_user.role)
    return jsonify({"status": result, "data": param_info})


@develop_api_view.route("/add/body/", methods=["POST"])
@login_required
def add_body_param():
    request_form = request.form
    param = request_form["param"]
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    type = request_form["type"]
    result, param_info = control.add_body_param(current_user.account, api_no, param, necessary, type, desc, current_user.role)
    if result is False:
        return param_info
    return json.dumps({"status": True, "data": param_info})


@develop_api_view.route("/add/input/", methods=["POST"])
@login_required
def add_input_example():
    request_form = request.form
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    example = request_form["example"]
    result, input_info = control.add_input_example(current_user.account, api_no, example, desc, current_user.role)
    if result is False:
        return input_info
    return json.dumps({"status": True, "data": input_info})


@develop_api_view.route("/add/output/", methods=["POST"])
@login_required
def add_output_example():
    request_form = request.form
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    example = request_form["example"]
    result, output_info = control.add_output_example(current_user.account, api_no, example, desc, current_user.role)
    if result is False:
        return output_info
    return json.dumps({"status": True, "data": output_info})


@develop_api_view.route("/care/", methods=["POST", "DELETE"])
@login_required
def add_care():
    request_form = request.form
    api_no = request_form["api_no"]
    if request.method == "POST":
        result, care_info = control.add_care(api_no, current_user.account, current_user.role)
    else:
        result, care_info = control.delete_care(api_no, current_user.account)
    return json.dumps({"status": result, "data": care_info})


@develop_api_view.route("/delete/<api_no>/", methods=["GET"])
@login_required
def delete_api(api_no):
    result, data = control.delete_api(api_no, current_user.account)
    if result is False:
        return data
    return redirect(url_for("develop_api_view.list_api"))


@develop_api_view.route("/delete/header/", methods=["DELETE"])
@login_required
def delete_header():
    request_data = request.json
    if "api_no" in request_data and "param" in request_data:
        result, data = control.delete_header(current_user.role, request_data["api_no"], request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/delete/body/", methods=["DELETE"])
@login_required
def delete_body():
    request_data = request.json
    if "api_no" in request_data and "param" in request_data:
        result, data = control.delete_body(current_user.role, request_data["api_no"], request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/delete/input/<input_no>/", methods=["DELETE"])
@login_required
def delete_input(input_no):
    result, data = control.delete_input(input_no, current_user.role)
    return json.dumps({"status": result, "data": data})


@develop_api_view.route("/delete/output/<output_no>/", methods=["DELETE"])
@login_required
def delete_output(output_no):
    result, data = control.delete_ouput(output_no, current_user.role)
    return json.dumps({"status": result, "data": data})


@develop_api_view.route("/update/header/", methods=["PUT"])
@login_required
def update_api_predefine_header():
    if "Referer" not in request.headers:
        return jsonify({"status": False, "data": "Bad Request"})
    ref_url = request.headers["Referer"]
    find_result = re.findall("api_no=([a-z\d]{32})", ref_url)
    if len(find_result) < 0:
        return jsonify({"status": False, "data": "Bad Request."})
    api_no = find_result[0]
    param = request.form["param"]
    update_type = request.form["update_type"]
    if update_type == "delete":
        result, message = control.delete_predefine_param(current_user.role, api_no, param)
    else:
        result, message = control.add_predefine_header(current_user.account, api_no, param, current_user.role)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/test/", methods=["GET"])
@login_required
def test_api():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no, current_user.role)
    if result is False:
        return api_info
    if "Referer" in request.headers:
        return_url = request.headers["Referer"]
    else:
        return_url = url_prefix + "/info/?api_no=%s" % api_no
    status_url = url_prefix + "/status/"
    return render_template("%s/Test_API.html" % html_dir, api_info=api_info, return_url=return_url, api_no=api_no,
                           status_url=status_url)
