#! /usr/bin/env python
# coding: utf-8
import sys
from flask import request, jsonify, g, redirect

from Class import mongo_host
from Class.DistKey import DistKey

from Web import dist_key_prefix as url_prefix, create_blue

sys.path.append('..')

__author__ = 'Zhouheng'

dist_key_view = create_blue('dist_key_view', url_prefix=url_prefix)

dt = DistKey(mongo_host)


@dist_key_view.before_request
def before_request():
    print(g.user_roles)
    print(g.request_IP_s)


@dist_key_view.route("/", methods=["GET"])
def get_key():
    if "app" not in request.args:
        return jsonify({"status": False, "data": "need app"})
    app = request.args["app"]
    keys = dt.select(app)
    print(app)
    return jsonify({"status": True, "data": keys})
