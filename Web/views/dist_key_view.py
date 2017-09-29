#! /usr/bin/env python
# coding: utf-8
import sys

from flask import request, jsonify, g, redirect, make_response
from flask_login import login_required
from Tools.RenderTemplate import RenderTemplate
from Class import mongo_host
from Class.DistKey import DistKey

from Web import dist_key_prefix as url_prefix, create_blue

sys.path.append('..')

__author__ = 'Zhouheng'

rt = RenderTemplate("Dist_Key", url_prefix=url_prefix)

dist_key_view = create_blue('dist_key_view', url_prefix=url_prefix, auth_required=False)

dt = DistKey(mongo_host)


@dist_key_view.before_request
def before_request():

    @login_required
    def web_access():
        if "dist_key" not in g.user_roles:
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
def get_key():
    if "app" not in request.args:
        query_url = url_prefix + "/query/"
        return rt.render("index.html", query_url=query_url)
    app = request.args["app"]
    keys = dt.select(app)
    print(app)
    return jsonify({"status": True, "data": keys})


@dist_key_view.route("/query/", methods=["POST"])
def query_users_key():
    r_data = request.json
    if r_data is None:
        r_data = dict()
    keys = dt.select2(g.user_name, **r_data)
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

