#! /usr/bin/env python
# coding: utf-8
import sys
from time import time

from flask import request, jsonify, g, make_response
from flask_login import login_required
from Tools.RenderTemplate import RenderTemplate
from Class.Performance import PerformanceManager
from Function.Common import unix_timestamp

from Web import performance_prefix as url_prefix, create_blue, dms_url_prefix

sys.path.append('..')

__author__ = 'Zhouheng'

rt = RenderTemplate("Performance", url_prefix=url_prefix)
performance_man = PerformanceManager()
performance_view = create_blue('performance_view', url_prefix=url_prefix, auth_required=False)

m_1 = dict(module_no=1, module_name="需求", score=1, weighted_score=2)
m_2 = dict(module_no=2, module_name="二次需求", score=0.4, weighted_score=0.8)
m_3 = dict(module_no=3, module_name="任务", score=0.25, weighted_score=0.5)
m_4 = dict(module_no=4, module_name="技术", score=1, weighted_score=2)
m_5 = dict(module_no=5, module_name="BUG响应", score=0.25, weighted_score=0.5)
m_s = [m_1, m_2, m_3, m_4, m_5]


@performance_view.before_request
def before_request():

    @login_required
    def web_access():
        if g.user_roles is None or "dist_key" not in g.user_roles:
            return make_response("无权限", 403)

    def api_access():
        if request.method != "GET":
            return make_response("Not Allow", 403)

    if request.headers.get("User-Agent") != "jyrequests":
        return web_access()
    else:
        return api_access()


@performance_view.route("/", methods=["GET"])
def get_one_key():
    if "app" not in request.args:
        query_url = url_prefix + "/query/"
        module_url = url_prefix + "/module/"
        list_user_url = dms_url_prefix + "/user/"
        return rt.render("index.html", query_url=query_url, module_url=module_url, list_user_url=list_user_url)
    return jsonify({"status": False, "data": "No Key"})


@performance_view.route("/module/", methods=["GET"])
def get_module_info():
    return jsonify({"status": True, "data": m_s})


@performance_view.route("/query/", methods=["POST"])
def query_users_key():
    return jsonify({"status": True, "data": []})


@performance_view.route("/", methods=["POST"])
def new_performance():
    r_data = request.json
    name = r_data["name"]
    detail_info = r_data["detail_info"]
    start_time = r_data["start_time"]
    end_time = r_data["end_time"]
    month = unix_timestamp(end_time, "month")
    module = r_data["module"]
    current_module = None
    for item in m_s:
        if module == item["module_no"]:
            current_module = item
            break
    if current_module is None:
        return jsonify({"status": True, "data": "success"})
    basic_data = performance_man.insert_performance(name, detail_info, start_time, end_time, g.user_name)
    if basic_data is None:
        return jsonify({"status": True, "data": "success"})
    related_data = performance_man.insert_module_related(month, module, basic_data["id"])
    if related_data is None:
        return jsonify({"status": True, "data": "success"})
    basic_data.update(related_data)
    members = r_data["members"]
    for m_item in members:
        score = current_module["weighted_score"] if m_item["is_weighted"] is True else current_module["score"]
        performance_man.insert_members(basic_data["id"], m_item["user_name"], score * 1000)
    return jsonify({"status": True, "data": "success"})

