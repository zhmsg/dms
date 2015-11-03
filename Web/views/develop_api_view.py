#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import Blueprint, render_template, send_from_directory, request
from Class.Control import ControlManager

sys.path.append('..')

__author__ = 'Zhouheng'


develop_api_view = Blueprint('develop_api_view', __name__)

control = ControlManager()


@develop_api_view.app_errorhandler(500)
def handle_500(e):
    return str(e.args)


@develop_api_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_api_view.route("/new/", methods=["GET"])
def new_api_page():
    result, module_list = control.get_module_list()
    if result is False:
        return module_list
    return render_template("/Dev/API_HELP/New_API.html", module_list=module_list)

