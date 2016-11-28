#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import render_template, request, g, jsonify
from flask_login import current_user

from Web import dev_url_prefix, create_blue
from Web import control, data_dir

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Dev"
backup_dir = "%s/back_table" % data_dir
url_prefix = dev_url_prefix

develop_view = create_blue('develop_view', url_prefix=url_prefix)


@develop_view.route("/operate/auth/", methods=["GET"])
def operate_auth_show():
    result, data = control.show_operate_auth(current_user.role)
    if result is False:
        return data
    return render_template("%s/operate_auth.html" % html_dir, operate_auth=data, url_prefix=url_prefix)


@develop_view.route("/data/table/", methods=["GET"])
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
    return render_template("%s/data_table.html" % html_dir, table_list=table_list, column_info=column_info,
                           select_table=select_table, query_str=query_str, url_prefix=url_prefix)


@develop_view.route("/data/table/backup/", methods=["POST"])
def backup_table_func():
    t_name = request.json["t_name"]
    sql_path = "%s/%s.sql.backup" % (backup_dir, t_name)
    result, info = control.backup_table(g.user_name, g.user_role, t_name, sql_path)
    return jsonify({"status": result, "data": info})