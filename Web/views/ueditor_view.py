#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from flask import request, jsonify, send_from_directory
from Tools.RenderTemplate import RenderTemplate
from Web import editor_url_prefix as url_prefix, create_blue

rt = RenderTemplate("UEditor", url_prefix=url_prefix)
editor_view = create_blue('editor_view', url_prefix=url_prefix)


@editor_view.route("/")
def demo_func():
    return rt.render("demo.html")


@editor_view.route("/config/")
def config_func():
    action = request.args["action"]
    return rt.render("config.json")


def send_editor_static_file(filename):
    return send_from_directory("ueditor", filename)


editor_view.add_url_rule('/<path:filename>', endpoint='ueditor', view_func=send_editor_static_file)
