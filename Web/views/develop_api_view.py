#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import json
import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, g
from flask_login import login_required, current_user
from Web import api_url_prefix, data_dir
from Web.views import control


sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = api_url_prefix
html_dir = "/API_HELP"
case_dir = "%s/test_case" % data_dir
if os.path.isdir(case_dir) is False:
    os.mkdir(case_dir)

develop_api_view = Blueprint('develop_api_view', __name__)


print("start success")


@develop_api_view.before_request
@login_required
def before_request():
    pass


def referer_api_no(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Referer" not in request.headers:
            return jsonify({"status": False, "data": "Bad Request"})
        g.ref_url = request.headers["Referer"]
        find_result = re.findall("api_no=([a-z\d]{32})", g.ref_url)
        if len(find_result) < 0:
            return jsonify({"status": False, "data": "Bad Request."})
        g.api_no = find_result[0]
        return f(*args, **kwargs)
    return decorated_function


@develop_api_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_api_view.route("/")
def list_api():
    result, module_list = control.get_module_list(current_user.role)
    if result is False:
        return module_list
    if current_user.role & control.role_value["api_module_new"] == control.role_value["api_module_new"]:
        new_power = True
    else:
        new_power = False
    result, test_env = control.get_test_env(current_user.role)
    if result is False:
        return test_env
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
        module_env_info = []
        if "update" in request.args and request.args["update"] == "true" and new_power is True:
            module_env = current_module["module_env"]
            if module_env is not None:
                module_env_s = module_env.split("|")
                env_len = len(test_env)
                for i in range(env_len-1, -1, -1):
                    env = test_env[i]
                    if "%s" % env["env_no"] in module_env_s:
                        module_env_info.append(env)
                        test_env.remove(env)
            return render_template("%s/Update_API_Module.html" % html_dir, module_list=module_list, api_list=module_data["api_list"],
                                   current_module=current_module, url_prefix=url_prefix, test_env=test_env,
                                   module_env_info=module_env_info)
        my_care = None
        for item in module_data["care_info"]:
            if item["user_name"] == current_user.account:
                my_care = item
                module_data["care_info"].remove(item)
                break
        return render_template("%s/List_Module_API.html" % html_dir, module_list=module_list, api_list=module_data["api_list"],
                               current_module=current_module, url_prefix=url_prefix, new_power=new_power,
                               my_care=my_care, care_info=module_data["care_info"])
    return render_template("%s/New_API_Module.html" % html_dir, module_list=module_list, url_prefix=url_prefix,
                           new_power=new_power, test_env=test_env)


@develop_api_view.route("/module/", methods=["POST"])
def new_api_module():
    request_data = request.json
    module_name = request_data["module_name"]
    module_prefix = request_data["module_prefix"]
    module_desc = request_data["module_desc"]
    module_part = request_data["module_part"]
    module_env = request_data["module_env"]
    result, message = control.new_api_module(current_user.role, module_name, module_prefix, module_desc, module_part, module_env)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/module/<int:module_no>/", methods=["POST"])
def update_api_module(module_no):
    request_data = request.json
    module_name = request_data["module_name"]
    module_prefix = request_data["module_prefix"]
    module_desc = request_data["module_desc"]
    module_part = request_data["module_part"]
    module_env = request_data["module_env"]
    result, message = control.update_api_module(current_user.role, module_no, module_name, module_prefix, module_desc, module_part, module_env)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/module/care/", methods=["POST", "DELETE"])
def add_module_care():
    request_form = request.form
    module_no = int(request_form["module_no"])
    if request.method == "POST":
        result, care_info = control.add_module_care(current_user.account, current_user.role, module_no)
    else:
        result, care_info = control.delete_module_care(current_user.account, module_no)
    return json.dumps({"status": result, "data": care_info})


@develop_api_view.route("/info/", methods=["GET"])
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
@referer_api_no
def set_api_completed():
    api_no = g.api_no
    result, info = control.set_api_completed(current_user.account, current_user.role, api_no)
    if result is False:
        return info
    return redirect(g.ref_url)


@develop_api_view.route("/update/modify/", methods=["GET"])
@referer_api_no
def set_api_modify():
    api_no = g.api_no
    result, info = control.set_api_modify(current_user.account, current_user.role, api_no)
    if result is False:
        return info
    return redirect(g.ref_url)


@develop_api_view.route("/add/header/", methods=["POST"])
def add_header_param():
    request_form = request.form
    param = request_form["param"]
    api_no = request_form["api_no"]
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    result, param_info = control.add_header_param(current_user.account, api_no, param, necessary, desc, current_user.role)
    return jsonify({"status": result, "data": param_info})


@develop_api_view.route("/add/body/", methods=["POST"])
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
def add_care():
    request_form = request.form
    api_no = request_form["api_no"]
    if request.method == "POST":
        result, care_info = control.add_care(api_no, current_user.account, current_user.role)
    else:
        result, care_info = control.delete_care(api_no, current_user.account)
    return json.dumps({"status": result, "data": care_info})


@develop_api_view.route("/delete/<api_no>/", methods=["GET"])
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
def delete_body():
    request_data = request.json
    if "api_no" in request_data and "param" in request_data:
        result, data = control.delete_body(current_user.role, request_data["api_no"], request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/delete/input/<input_no>/", methods=["DELETE"])
def delete_input(input_no):
    result, data = control.delete_input(input_no, current_user.role)
    return json.dumps({"status": result, "data": data})


@develop_api_view.route("/delete/output/<output_no>/", methods=["DELETE"])
def delete_output(output_no):
    result, data = control.delete_ouput(output_no, current_user.role)
    return json.dumps({"status": result, "data": data})


@develop_api_view.route("/update/header/", methods=["PUT"])
@referer_api_no
def update_api_predefine_header():
    api_no = g.api_no
    param = request.form["param"]
    update_type = request.form["update_type"]
    if update_type == "delete":
        result, message = control.delete_predefine_param(current_user.role, api_no, param)
    else:
        result, message = control.add_predefine_header(current_user.account, api_no, param, current_user.role)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/test/", methods=["GET"])
def test_api():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no, current_user.role)
    if result is False:
        return api_info
    module_test_env = []
    if api_info["basic_info"]["module_env"] is not None:
        module_env_s = api_info["basic_info"]["module_env"].split("|")
        env_no_list = []
        for env_no_s in module_env_s:
            env_no_list.append(int(env_no_s))
        result, module_test_env = control.get_test_env(current_user.role, env_no_list)
        if result is False:
            return module_test_env
    if "Referer" in request.headers:
        return_url = request.headers["Referer"]
    else:
        return_url = url_prefix + "/info/?api_no=%s" % api_no
    status_url = url_prefix + "/status/"
    test_case_url = url_prefix + "/test/case/"
    api_url = api_info["basic_info"]["api_url"]
    url_params = re.findall("<([\w:]+)>", api_url)
    url_param_info = []
    for param in url_params:
        param_sp = param.split(":")
        if len(param_sp) > 1:
            url_param_info.append({"param_type": param_sp[0], "param_name": param_sp[1], "origin_param": "<%s>" % param})
        else:
            url_param_info.append({"param_type": "string", "param_name": param_sp[0], "origin_param": "<%s>" % param})
    return render_template("%s/Test_API.html" % html_dir, api_info=api_info, return_url=return_url, api_no=api_no,
                           status_url=status_url, url_param_info=url_param_info, module_test_env=module_test_env,
                           test_case_url=test_case_url)


@develop_api_view.route("/test/case/", methods=["POST"])
@referer_api_no
def add_test_case():
    r_data = request.json
    api_no = g.api_no
    case_name = r_data["case_name"]
    user_case_dir = "%s/%s" % (case_dir, current_user.account)
    if os.path.isdir(user_case_dir) is False:
        os.mkdir(user_case_dir)
    case_file = "%s_%s" % (api_no, case_name)
    case_path = "%s/%s.case" % (user_case_dir, case_file)
    with open(case_path, "w") as cw:
        cw.write(json.dumps(r_data, indent=2))
    return jsonify({"status": True, "data": "success"})


@develop_api_view.route("/test/case/", methods=["GET"])
@referer_api_no
def list_test_case():
    api_no = g.api_no
    user_case_dir = "%s/%s" % (case_dir, current_user.account)
    if os.path.isdir(user_case_dir) is False:
        return jsonify({"status": True, "data": []})
    case_files = os.listdir(user_case_dir)
    api_test_case = []
    for item in case_files:
        if item.startswith(api_no):
            api_test_case.append(item[33:-5])
    return jsonify({"status": True, "data": api_test_case})


@develop_api_view.route("/test/case/<case_name>/", methods=["GET"])
@referer_api_no
def test_case_content(case_name):
    api_no = g.api_no
    user_case_dir = "%s/%s" % (case_dir, current_user.account)
    case_path = "%s/%s_%s.case" % (user_case_dir, api_no, case_name)
    if os.path.isfile(case_path) is False:
        return jsonify({"status": False, "data": "not exist"})
    case_info = {}
    with open(case_path, "r") as cr:
        content = cr.read()
        case_info = json.loads(content)
    return jsonify({"status": True, "data": case_info})