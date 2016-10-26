#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, g
from Web import api_url_prefix, create_blue, test_url_prefix
from Web import control


sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = api_url_prefix
html_dir = "/API_HELP"


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


@develop_api_view.route("/", methods=["GET"])
def list_api():
    result, part_module = control.get_part_api(g.user_name, g.user_role)
    if result is False:
        return part_module
    if g.user_role & control.role_value["api_module_new"] == control.role_value["api_module_new"]:
        new_power = True
    else:
        new_power = False
    result, test_env = control.get_test_env(g.user_role)
    if result is False:
        return test_env
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
        result, module_data = control.get_api_list(module_no, g.user_role)
        if result is False:
            return module_data
        current_module = None
        for part in part_module:
            for module_info in part["module_list"]:
                if module_info["module_no"] == module_no:
                    current_module = module_info
                    current_module["part_no"] = part["part_no"]
                    current_module["part_name"] = part["part_name"]
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
            return render_template("%s/Update_API_Module.html" % html_dir, part_module=part_module, api_list=module_data["api_list"],
                                   current_module=current_module, url_prefix=url_prefix, test_env=test_env,
                                   module_env_info=module_env_info)
        my_care = None
        for item in module_data["care_info"]:
            if item["user_name"] == g.user_name:
                my_care = item
                module_data["care_info"].remove(item)
                break
        test_module_url = test_url_prefix + "/batch/"
        return render_template("%s/List_Module_API.html" % html_dir, part_module=part_module, api_list=module_data["api_list"],
                               current_module=current_module, url_prefix=url_prefix, new_power=new_power,
                               my_care=my_care, care_info=module_data["care_info"], test_module_url=test_module_url)
    return render_template("%s/New_API_Module.html" % html_dir, part_module=part_module, url_prefix=url_prefix,
                           new_power=new_power, test_env=test_env)


@develop_api_view.route("/", methods=["POST"])
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
    result, api_info = control.new_api_info(module_no, title, url, method, desc, g.user_name, g.user_role)
    if result is False:
        return api_info
    return redirect(url_prefix + "/update/info/?api_no=%s" % api_info["api_no"])


@develop_api_view.route("/module/", methods=["GET"])
def get_module_api():
    if "module_no" not in request.args:
        return jsonify({"status": False, "data": "Need module_no"})
    module_no = int(request.args["module_no"])
    result, module_data = control.get_api_list(module_no, g.user_role)
    return jsonify({"status": result, "data": module_data})


@develop_api_view.route("/module/", methods=["POST", "PUT"])
def new_api_module():
    request_data = request.json
    module_name = request_data["module_name"]
    module_prefix = request_data["module_prefix"]
    module_desc = request_data["module_desc"]
    module_part = request_data["module_part"]
    module_env = request_data["module_env"]
    if request.method == "POST":
        result, message = control.new_api_module(g.user_role, module_name, module_prefix, module_desc, module_part, module_env)
    else:
        module_no = request_data["module_no"]
        result, message = control.update_api_module(g.user_role, module_no, module_name, module_prefix, module_desc, module_part, module_env)
    return jsonify({"status": result, "data": message})


@develop_api_view.route("/module/care/", methods=["POST", "DELETE"])
def add_module_care():
    request_data = request.json
    module_no = request_data["module_no"]
    if request.method == "POST":
        result, care_info = control.add_module_care(g.user_name, g.user_role, module_no)
    else:
        result, care_info = control.delete_module_care(g.user_name, module_no)
    return jsonify({"status": result, "data": care_info})


@develop_api_view.route("/info/", methods=["GET"])
def show_api():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = control.get_api_info(api_no, g.user_role)
    if result is False:
        return api_info
    return_url = url_prefix + "/?module_no=%s" % api_info["basic_info"]["module_no"]
    update_url = None
    test_url = url_prefix + "/test/?api_no=%s" % api_no
    batch_test_url = None
    if g.user_role & control.role_value["api_new"] == control.role_value["api_new"]:
        update_url = url_prefix + "/update/info/?api_no=%s" % api_no
        batch_test_url = url_prefix + "/test/batch/?api_no=%s" % api_no
    status_url = url_prefix + "/status/"
    my_care = None
    for item in api_info["care_info"]:
        if item["user_name"] == g.user_name:
            my_care = item
            api_info["care_info"].remove(item)
            break
    if "X-Requested-With" in request.headers:
        if request.headers["X-Requested-With"] == "XMLHttpRequest":
            return jsonify({"status": True, "data": {"api_info": api_info}})
    return render_template("%s/Show_API.html" % html_dir, api_info=api_info, api_no=api_no, return_url=return_url,
                           update_url=update_url, my_care=my_care, test_url=test_url, url_prefix=url_prefix,
                           status_url=status_url, batch_test_url=batch_test_url)


@develop_api_view.route("/basic/", methods=["GET"])
def new_api_page():
    result, part_module = control.get_part_api(g.user_name, g.user_role)
    if result is False:
        return part_module
    if "api_no" in request.args:
        api_no = request.args["api_no"]
        if len(api_no) != 32:
            return "Bad api_no"
        result, part_module = control.get_part_api(g.user_name, g.user_role)
        if result is False:
            return part_module
        result, api_info = control.get_api_info(api_no, g.user_role)
        return_url = url_prefix + "/info/?api_no=%s" % api_no
        if result is False:
            return api_info
        module_no = api_info["basic_info"]["module_no"]
        return render_template("%s/New_API.html" % html_dir, part_module=part_module, url_prefix=url_prefix,
                               module_no=module_no, api_info=api_info, return_url=return_url)
    module_no = 1
    if "module_no" in request.args:
        module_no = int(request.args["module_no"])
    return render_template("%s/New_API.html" % html_dir, part_module=part_module, url_prefix=url_prefix,
                           module_no=module_no)


@develop_api_view.route("/basic/", methods=["POST"])
def update_api_info():
    request_form = request.form
    api_module = request_form["api_module"]
    api_no = request_form["api_no"]
    desc = request_form["api_desc"]
    url = request_form["api_url"]
    title = request_form["api_title"]
    method = request_form["api_method"]
    module_no = int(api_module)
    result, message = control.update_api_info(role=g.user_role, api_no=api_no, desc=desc, method=method,
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
    result, api_info = control.get_api_info(api_no, g.user_role)
    return_url = url_prefix + "/info/?api_no=%s" % api_no
    if result is False:
        return api_info
    return render_template("%s/Update_API.html" % html_dir, api_info=api_info, api_no=api_no, return_url=return_url,
                           url_prefix=url_prefix)


@develop_api_view.route("/status/<int:api_status>/", methods=["GET"])
@referer_api_no
def update_api_status_func(api_status):
    api_no = g.api_no
    result, info = control.set_api_status(g.user_name, g.user_role, api_no, api_status)
    if result is False:
        return info
    return redirect(g.ref_url)


@develop_api_view.route("/header/", methods=["POST"])
@referer_api_no
def add_header_param():
    request_form = request.json
    param = request_form["name"]
    api_no = g.api_no
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    result, param_info = control.add_header_param(g.user_name, api_no, param, necessary, desc, g.user_role)
    return jsonify({"status": result, "data": param_info})


@develop_api_view.route("/body/", methods=["POST"])
@referer_api_no
def add_body_param():
    request_form = request.json
    param = request_form["name"]
    api_no = g.api_no
    desc = request_form["desc"]
    necessary = int(request_form["necessary"])
    type = request_form["type"]
    result, param_info = control.add_body_param(g.user_name, api_no, param, necessary, type, desc, g.user_role)
    if result is False:
        return param_info
    return jsonify({"status": True, "data": param_info})


@develop_api_view.route("/input/", methods=["POST"])
@referer_api_no
def add_input_example():
    request_form = request.json
    api_no = g.api_no
    desc = request_form["desc"]
    example = request_form["example"]
    result, input_info = control.add_input_example(g.user_name, api_no, example, desc, g.user_role)
    if result is False:
        return input_info
    return jsonify({"status": True, "data": input_info})


@develop_api_view.route("/output/", methods=["POST"])
@referer_api_no
def add_output_example():
    request_form = request.json
    api_no = g.api_no
    desc = request_form["desc"]
    example = request_form["example"]
    result, output_info = control.add_output_example(g.user_name, api_no, example, desc, g.user_role)
    if result is False:
        return output_info
    return jsonify({"status": True, "data": output_info})


@develop_api_view.route("/care/", methods=["POST", "DELETE"])
def add_care():
    request_data = request.json
    api_no = request_data["api_no"]
    if request.method == "POST":
        result, care_info = control.add_care(api_no, g.user_name, g.user_role)
    else:
        result, care_info = control.delete_care(api_no, g.user_name)
    return jsonify({"status": result, "data": care_info})


@develop_api_view.route("/delete/<api_no>/", methods=["GET"])
def delete_api(api_no):
    result, data = control.delete_api(api_no, g.user_name)
    if result is False:
        return data
    return redirect(url_for("develop_api_view.list_api"))


@develop_api_view.route("/header/", methods=["DELETE"])
def delete_header():
    request_data = request.json
    if "api_no" in request_data and "param" in request_data:
        result, data = control.delete_header(g.user_role, request_data["api_no"], request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/body/", methods=["DELETE"])
def delete_body():
    request_data = request.json
    if "api_no" in request_data and "param" in request_data:
        result, data = control.delete_body(g.user_role, request_data["api_no"], request_data["param"])
        return jsonify({"status": result, "data": data})
    return jsonify({"status": False, "data": "need api_no and param"})


@develop_api_view.route("/input/<input_no>/", methods=["DELETE"])
def delete_input(input_no):
    result, data = control.delete_input(input_no, g.user_role)
    return jsonify({"status": result, "data": data})


@develop_api_view.route("/output/<output_no>/", methods=["DELETE"])
def delete_output(output_no):
    result, data = control.delete_ouput(output_no, g.user_role)
    return jsonify({"status": result, "data": data})


@develop_api_view.route("/update/header/", methods=["PUT"])
@referer_api_no
def update_api_predefine_header():
    api_no = g.api_no
    param = request.form["param"]
    update_type = request.form["update_type"]
    param_type = request.form["param_type"]
    if update_type == "delete":
        result, message = control.delete_predefine_param(g.user_role, api_no, param)
    else:
        result, message = control.add_predefine_header(g.user_name, api_no, param, param_type, g.user_role)
    return jsonify({"status": result, "data": message})
