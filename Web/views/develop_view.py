#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import Blueprint, render_template, send_from_directory, request
from flask_login import current_user, login_required

from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'


develop_view = Blueprint('develop_view', __name__)


@develop_view.app_errorhandler(500)
def handle_500(e):
    return str(e.args)


@develop_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_view.route("/operate/auth/", methods=["GET"])
@login_required
def operate_auth_show():
    result, data = control.show_operate_auth(current_user.role)
    if result is False:
        return data
    return render_template("/Dev/operate_auth.html", operate_auth=data)


@develop_view.route("/operate/auth/download/", methods=["GET"])
@login_required
def download_operate_auth():
    result, data = control.download_operate_auth(current_user.role)
    if result is True:
        return send_from_directory(data["DIR"], data["FILE"], as_attachment=True)
    return data


@develop_view.route("/data/table/", methods=["GET"])
@login_required
def show_data_table():
    result, table_list = control.list_data_table(current_user.role)
    if result is False:
        return table_list
    column_info = []
    select_table = {}
    if "table" in request.args:
        result, column_info = control.get_table_info(request.args["table"], current_user.role)
        if result is False:
            return column_info
        for table in table_list:
            if table["table_name"] == request.args["table"]:
                select_table = table
                break
    query_str = ""
    if "query" in request.args:
        query_str = request.args["query"]
    return render_template("/Dev/data_table.html", table_list=table_list, column_info=column_info,
                           select_table=select_table, query_str=query_str)
