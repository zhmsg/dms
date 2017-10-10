#! /usr/bin/env python
# coding: utf-8
import sys
from time import time

from flask import request, jsonify, g, redirect, make_response
from flask_login import login_required
from Tools.RenderTemplate import RenderTemplate
from Class import mongo_host
from Class.DistKey import DistKey
from Class.IP import IPManager

from Web import dist_key_prefix as url_prefix, create_blue, tools_url_prefix

sys.path.append('..')

__author__ = 'Zhouheng'

rt = RenderTemplate("Dist_Key", url_prefix=url_prefix)

dist_key_view = create_blue('dist_key_view', url_prefix=url_prefix, auth_required=False)

dt = DistKey(mongo_host)
ip_man = IPManager()


@dist_key_view.before_request
def before_request():

    @login_required
    def web_access():
        if g.user_roles is None or "dist_key" not in g.user_roles:
            return make_response("无权限", 403)

    def api_access():
        if request.method != "GET":
            return make_response("Not Allow", 403)

    print(g.request_IP_s)
    if request.headers.get("User-Agent") != "jyrequests":
        return web_access()
    else:
        return api_access()


@dist_key_view.route("/", methods=["GET"])
def get_one_key():
    if "app" not in request.args:
        query_url = url_prefix + "/query/"
        ip_group_url = tools_url_prefix + "/ip/group/"
        return rt.render("index.html", query_url=query_url, ip_group_url=ip_group_url)
    kwargs = dict()
    for item in request.args:
        if item[0] == "_":
            continue
        kwargs[item] = request.args[item]
    kwargs.update(dict(ip_auth=True))
    keys = dt.select(**kwargs)
    for item in keys:
        if isinstance(item.get("ip_groups"), list) is False:
            continue
        for g_name in item["ip_groups"]:
            if len(ip_man.query(g_name, g.request_IP)) > 0 and item["deadline"] > time() + 24 * 60 * 60:
                item["deadline"] = int(time()) + 24 * 60 * 60
                return jsonify({"status": True, "data": item})
    return jsonify({"status": False, "data": "No Key"})


@dist_key_view.route("/query/", methods=["POST"])
def query_users_key():
    r_data = request.json
    if r_data is None:
        r_data = dict()
    keys = dt.select2(g.user_name, **r_data)
    for item in keys:
        for sk in item:
            if sk[0] == "_":
                item[sk] = "*" * len(item[sk])
    return jsonify({"status": True, "data": keys})


@dist_key_view.route("/", methods=["POST"])
def add_key():
    r_data = request.json
    app = r_data["app"]
    deadline = int(r_data["deadline"])
    ip_auth = r_data["ip_auth"]
    del r_data["app"]
    del r_data["deadline"]
    del r_data["ip_auth"]
    if "user_name" in r_data:
        del r_data["user_name"]
    dt.insert(app, deadline, g.user_name, ip_auth=ip_auth, **r_data)
    return jsonify({"status": True, "data": "success"})


@dist_key_view.route("/", methods=["PUT"])
def update_key():
    r_data = request.json
    id = r_data["id"]
    kwargs = dict()
    if "offset" in r_data:
        kwargs["offset"] = int(r_data["offset"])
    elif "deadline" in r_data:
        kwargs["deadline"] = r_data["deadline"]
    else:
        return jsonify({"status": True, "data": []})
    data = dt.update_deadline(id, g.user_name, **kwargs)
    if data is not None:
        data["id"] = str(data["_id"])
        del data["_id"]
        return jsonify({"status": True, "data": [data]})
    return jsonify({"status": True, "data": []})