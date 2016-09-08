#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import render_template, request, jsonify, g
from flask_login import login_required, current_user

from Web import log_url_prefix as url_prefix, ip, my_email, company_ip_required, create_blue, status_url_prefix
from Web import unix_timestamp, ip_str, dms_scheduler, env, dms_job
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/LOG"

jy_log_view = create_blue('jy_log_view', url_prefix=url_prefix, auth_required=False)


@jy_log_view.route("/", methods=["GET"])
@login_required
@company_ip_required
def show_log_list():
    if "start_time" in request.args and request.args["start_time"] != "0":
        start_time = int(request.args["start_time"])
    else:
        start_time = None
    if "end_time" in request.args and request.args["end_time"] != "0":
        end_time = int(request.args["end_time"])
    else:
        end_time = None
    if "log_level" in request.args and request.args["log_level"] != "all":
        level = request.args["log_level"]
    else:
        level = None

    if "url_prefix" in request.args and request.args["url_prefix"] != "":
        search_url = request.args["url_prefix"]
    else:
        search_url = ""
    if "account" in request.args and request.args["account"] != "":
        search_account = request.args["account"]
    else:
        search_account = ""
    result, info = control.look_jy_log(current_user.account, current_user.role, start_time, end_time, level=level,
                                       search_url=search_url, search_account=search_account)
    if result is False:
        return info
    log_records = info["log_records"]
    return render_template("%s/Show_Log.html" % html_dir, log_list=log_records, url_prefix=url_prefix,
                           log_level=control.jy_log.log_level, current_level=level, search_url=search_url,
                           search_account=search_account, require=info["require"], status_url_prefix=status_url_prefix)


@jy_log_view.route("/login/", methods=["POST", "GET"])
def record_login():
    request_data = request.json
    server_ip = g.request_IP
    user_ip_s = request_data["login_ip"]
    user_ip = ip.ip_value_str(ip_str=user_ip_s)
    login_user = request_data["login_user"]
    login_time = request_data["login_time"]
    server_name = request_data["server_name"]
    result, info = control.new_login_server(server_ip, server_name, user_ip, login_user, login_time)
    trust_ip = ["123.7.182.111", "10.51.72.158", "10.44.147.192"]
    trust_user = ["msg", "wzh"]
    # if user_ip_s not in trust_ip or login_user not in trust_user:
    #     email_content = u"登录的服务器IP：%s<br>登录的服务器主机名：%s<br>登录者的IP：%s<br>登录用户：%s<br>登录时间：%s" \
    #                     % (g.request_IP_s, server_name, user_ip_s, login_user, login_time)
    #     my_email.send_mail_thread("zhouheng@gene.ac", u"有用户登录到服务器", email_content)
    return jsonify({"status": result, "data": info})


# 发送每日日志
def send_log_func():
    if env != "Production" and env != "Development":
        return
    result, info = control.get_daily_log()
    table_content = ""
    for item in info["log_records"]:
        tr_content = '<tr title="info: %s&#10;host: %s">' % (item["info"].replace(">", "&gt;").replace('"', "&quot;"), item["host"])
        tr_content += '<td name="run_begin" class="status_move">%s</td>\n' % unix_timestamp(item["run_begin"])
        tr_content += '<td name="request_url">%s</td>\n' % item["url"]
        tr_content += '<td>%s</td>' % item["method"]
        tr_content += '<td name="request_account">%s</td>\n' % item["account"]
        if item["level"] == "error":
            level_class = "redBg"
        elif item["level"] == "base_error":
            level_class = "orgBg"
        elif item["level"] == "bad_req":
            level_class = "yellowBg"
        elif item["level"] == "http_error":
            level_class = "greenBg"
        else:
            level_class = ""
        tr_content += '<td name="log_level" class="%s">%s</td>\n' % (level_class, item["level"])

        if item["run_time"] >= 1:
            tr_content += '<td class="redBg">%s</td>' % item["run_time"]
        elif item["run_time"] >= 0.5:
            tr_content += '<td class="orgBg">%s</td>' % item["run_time"]
        else:
            tr_content += '<td>%s</td>' % item["run_time"]
        tr_content += "\n"
        tr_content += '<td name="request_ip">%s</td>' % ip_str(item["ip"])
        tr_content += "\n"
        tr_content += '</tr>\n'
        table_content += tr_content
    with open("../Web/templates/LOG/Daily_Log.html") as rt:
        content = rt.read()
        content = content.replace("{{ TR }}", table_content.encode("utf-8"))
        control.send_daily_log(content)

dms_job.append({"func": "%s:send_log_func" % __name__, "trigger": "cron", "id": "send_daily_log", "hour": 8, "minute": "30", "replace_existing": True})
# dms_scheduler.add_job(send_log_func, trigger="cron", id="send_daily_log", hour=8, minute=30)
