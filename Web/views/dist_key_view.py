#! /usr/bin/env python
# coding: utf-8
import sys
from flask import request, jsonify, g, redirect

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
    if "user_roles" in g:
        print(g.user_roles)
    print(g.request_IP_s)


@dist_key_view.route("/", methods=["GET"])
def get_key():
    if "app" not in request.args:
        return rt.render("index.html")
    app = request.args["app"]
    keys = dt.select(app)
    print(app)
    return jsonify({"status": True, "data": keys})


@dist_key_view.route("/", methods=["POST"])
def add_key():
    pass

