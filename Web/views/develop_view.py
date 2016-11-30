#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import render_template, request, g, jsonify
from flask_login import current_user

from Web import dev_url_prefix, create_blue
from Web import control, data_dir, dms_job, current_env

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


# 每天0：30，备份线上数据表。
def backup_func():
    if current_env != "Production":
        print("Not Production")
        return
    result, info = control.register_backup_task()
    if result is False:
        print("register backup fail")
        return
    print("start run backup table task %s" % info["task_no"])
    allow_t = ["collect_variant", "health_examination_result", "health_examination_result_v3", "health_gift_result",
               "health_gift_result_v3", "health_report_survey", "health_survey_report", "health_survey_result",
               "log_project", "patient_info", "patient_test", "project_user_right", "sample_group", "sample_info",
               "sample_phenotype", "sample_report", "sample_user_right", "sys_patients", "sys_project_sample",
               "sys_projects", "sys_samples", "sys_users", "target_ratio_detail", "task_collect_variant", "test_value",
               "user_config", "user_geneset", "user_info", "user_task_list", "user_template", "variant_data_nums",
               "variant_data_pic", "variant_md5", "variant_remark"]
    for t_name in allow_t:
        sql_path = "%s/%s_%s.sql.backup" % (backup_dir, current_env, t_name)
        control.backup_table("system", 0, t_name, sql_path)
    print("backup success")

dms_job.append({"func": "%s:backup_func" % __name__, "trigger": "cron", "id": "backup_table", "day_of_week": "0-4", "hour": 9, "minute": 10})
