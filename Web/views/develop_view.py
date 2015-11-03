#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import Blueprint, render_template, send_from_directory, request
from Tools.MyEmail import MyEmailManager
from Class.User import UserManager
from Class.Control import ControlManager

sys.path.append('..')

__author__ = 'Zhouheng'


develop_view = Blueprint('develop_view', __name__)

control = ControlManager()


@develop_view.app_errorhandler(500)
def handle_500(e):
    return str(e.args)


@develop_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_view.route("/operate/auth/", methods=["GET"])
def operate_auth_show():
    result, data = control.show_operate_auth()
    if result is False:
        return data
    return render_template("/Dev/operate_auth.html", operate_auth=data)


@develop_view.route("/operate/auth/download/", methods=["GET"])
def download_operate_auth():
    result, data = control.download_operate_auth()
    if result is True:
        return send_from_directory(data["DIR"], data["FILE"], as_attachment=True)
    return data


@develop_view.route("/data/table/", methods=["GET"])
def show_data_table():
    table_list = control.list_data_table()
    column_info = []
    select_table = {}
    if "table" in request.args:
        column_info = control.get_table_info(request.args["table"])
        for table in table_list:
            if table["table_name"] == request.args["table"]:
                select_table = table
                break
    return render_template("/Dev/data_table.html", table_list=table_list, column_info=column_info, select_table=select_table)