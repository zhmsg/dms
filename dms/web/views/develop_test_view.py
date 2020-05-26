#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import re
from functools import wraps
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import test_url_prefix, api_url_prefix, status_url_prefix, data_dir, create_blue

from dms.utils.manager import Explorer

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = test_url_prefix
html_dir = "/API_HELP"
case_dir = "%s/test_case" % data_dir
# if os.path.isdir(case_dir) is False:
#     os.mkdir(case_dir)

api_man = Explorer.get_instance().get_object_manager("api_help")

rt = RenderTemplate("API_HELP", url_prefix=url_prefix)
develop_test_view = create_blue('develop_test_view', url_prefix=url_prefix)


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


@develop_test_view.route("/", methods=["GET"])
def test_api_page():
    if "api_no" not in request.args:
        return "Need api_no"
    api_no = request.args["api_no"]
    if len(api_no) != 32:
        return "Bad api_no"
    result, api_info = api_man.get_api_info(api_no)
    if result is False:
        return api_info
    module_test_env = []
    if api_info["basic_info"]["module_env"] is not None:
        module_env_s = api_info["basic_info"]["module_env"].split("|")
        env_no_list = []
        for env_no_s in module_env_s:
            env_no_list.append(int(env_no_s))
        result, module_test_env = api_man.get_test_env(env_no_list)
        if result is False:
            return module_test_env
    # if g.user_role & control.role_value["api_new"] == control.role_value["api_new"]:
    new_right = True
    # else:
    #     new_right = False
    api_info_url = api_url_prefix + "/info/"
    api_example_url = api_url_prefix + "/example/"
    status_url = status_url_prefix + "/"
    test_case_url = url_prefix + "/case/"
    api_url = api_info["basic_info"]["api_url"]

    return rt.render("Test_API.html", api_info=api_info, api_no=api_no, status_url=status_url,
                     module_test_env=module_test_env, test_case_url=test_case_url,
                     api_info_url=api_info_url, new_right=new_right, api_example_url=api_example_url)


@develop_test_view.route("/batch/", methods=["GET"])
def batch_test_api_page():
    # if g.user_role & control.role_value["api_new"] != control.role_value["api_new"]:
    #     return "用户无权限"
    api_no = None
    if "api_no" in request.args:
        api_no = request.args["api_no"]
        if len(api_no) != 32:
            return "Bad api_no"
    module_no = None
    if "module_no" in request.args:
        module_no = request.args["module_no"]
    api_info_url = api_url_prefix + "/info/"
    status_url = status_url_prefix + "/"
    test_case_url = url_prefix + "/case/"
    test_url = url_prefix + "/"
    env_info_url = url_prefix + "/env/"
    module_api_url = api_url_prefix + "/module/"
    return rt.render("Batch_Test_API.html", api_no=api_no, status_url=status_url, test_case_url=test_case_url,
                     test_url=test_url, api_info_url=api_info_url, env_info_url=env_info_url,
                     module_api_url=module_api_url, module_no=module_no, api_url_prefix=api_url_prefix)


@develop_test_view.route("/env", methods=["GET"])
def get_test_env():
    env_no_list = None
    if "env_no" in request.args:
        env_no_list = request.args["env_no"].split(",")
        env_no_list = [int(v) for v in env_no_list]
    result, env_info = api_man.get_test_env(env_no_list)
    return jsonify({"status": result, "data": env_info})


@develop_test_view.route("/env/", methods=["POST"])
def add_test_env():
    r_data = request.json
    result, env_info = api_man.new_test_env(r_data["env_name"], r_data["env_address"])
    return jsonify({"status": result, "data": env_info})


@develop_test_view.route("/case/", methods=["POST"])
@referer_api_no
def add_test_case():
    r_data = request.json
    api_no = g.api_no
    case_name = r_data["case_name"]
    user_case_dir = "%s/%s" % (case_dir, g.user_name)
    if os.path.isdir(user_case_dir) is False:
        os.mkdir(user_case_dir)
        os.chmod(user_case_dir, 0o777)
    case_file = "%s_%s" % (api_no, case_name)
    case_path = "%s/%s.case" % (user_case_dir, case_file)
    with open(case_path, "w") as cw:
        cw.write(json.dumps(r_data, indent=2))
    os.chmod(case_path, 0o666)
    return jsonify({"status": True, "data": "success"})


@develop_test_view.route("/case/", methods=["GET"])
@referer_api_no
def list_test_case():
    api_no = g.api_no
    user_case_dir = "%s/%s" % (case_dir, g.user_name)
    if os.path.isdir(user_case_dir) is False:
        return jsonify({"status": True, "data": {"api_no": api_no, "case": []}})
    case_files = os.listdir(user_case_dir)
    api_test_case = []
    for item in case_files:
        if item.startswith(api_no):
            api_test_case.append(item[33:-5])
    return jsonify({"status": True, "data": {"api_no": api_no, "case": api_test_case}})


@develop_test_view.route("/case/<case_name>/", methods=["GET"])
@referer_api_no
def test_case_content(case_name):
    api_no = g.api_no
    user_case_dir = "%s/%s" % (case_dir, g.user_name)
    case_path = "%s/%s_%s.case" % (user_case_dir, api_no, case_name)
    if os.path.isfile(case_path) is False:
        return jsonify({"status": False, "data": "not exist"})
    # case_info = {}
    with open(case_path, "r") as cr:
        content = cr.read()
        case_info = json.loads(content)
    case_info["api_no"] = api_no
    return jsonify({"status": True, "data": case_info})
