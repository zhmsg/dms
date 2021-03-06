#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from datetime import datetime, timedelta
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Web import release_url_prefix as url_prefix, create_blue, user_blacklist, dms_scheduler, current_env, dms_job
from Web import control


sys.path.append('..')

__author__ = 'Zhouheng'


rt = RenderTemplate("Release", url_prefix=url_prefix)
develop_release_view = create_blue('develop_release_view', url_prefix=url_prefix)


@develop_release_view.before_request
def before_request():
    now_time = datetime.now()
    now_hour = now_time.hour
    now_weekday = now_time.weekday()
    g.now_minute = now_time.minute
    g.role_value = control.role_value
    g.ihVIP = False
    if g.user_role & control.role_value["release_ih_V"] > 0 and "noVIP" not in request.args:
        g.ihVIP = True
    if g.ihVIP is True:
        g.release_period = True
    elif now_weekday == 2 and now_hour in [14, 15, 16, 17, 18] and 10 <= g.now_minute < 20:
        g.release_period = True
    elif now_weekday == 3 and now_hour in [8, 9, 10, 11, 12, 14, 15, 16] and 10 <= g.now_minute < 20:
        g.release_period = True
    else:
        g.release_period = False
        allow_url = [url_prefix + "/", url_prefix + "/task/"]
        if request.path not in allow_url or request.method != "GET":
            user_blacklist.append(g.user_name)
            return jsonify({"status": False, "data": u"非法时段"})
    g.now_time = now_time


@develop_release_view.route("/", methods=["GET"])
def index_func():
    context = {"url_task_list": url_prefix + "/task/"}
    return rt.render("Release_Main.html", **context)


def run_task(release_no):
    result, info = control.release_ih()
    if result is False:
        control.update_task(release_no, False)
    print(info)


def system_auto_release():
    print("auto release")
    if current_env != "Production":
        print("Not Production")
        return
    if datetime.now().weekday() == 2:  # only allow wednesday restart API
        service_list = [0, 1, 2]
    else:
        service_list = [2]
    for restart_service in service_list:
        result, info = control.new_task("system", 0, u"自动发布", restart_service, u"系统周一到周五每天12：10，18：10左右自动重新发布晶云测试环境")
        if result is True:
            release_no = info["release_no"]
            run_task(release_no)
            break
        else:
            print(info.encode("utf-8"))


@develop_release_view.route("/meisanggou/", methods=["GET"])
def admin_release():
    result, info = control.release_ih()
    return jsonify({"status": result, "data": info})


@develop_release_view.route("/task/", methods=["POST"])
def new_task():
    request_data = request.json
    # reason = request_data["reason"]
    reason_desc = ""
    restart_service = int(request_data["restart_service"])
    result, info = control.new_task(g.user_name, g.user_role, u"修复BUG", restart_service, reason_desc)
    if result is True:
        release_no = info["release_no"]
        wait_minute = 10 - g.now_minute % 10
        run_date = g.now_time + timedelta(minutes=wait_minute)
        dms_scheduler.add_job(id="run_release_%s" % release_no, func=run_task, args=[release_no], trigger="date",
                              run_date=run_date)
    return jsonify({"status": result, "data": info})


@develop_release_view.route("/task/", methods=["GET"])
def list_task():
    result, info = control.get_task(g.user_name, g.user_role)
    return jsonify({"status": result, "data": info})


@develop_release_view.route("/online/", methods=["POST"])
def release_online():
    request_data = request.json
    service = request_data["service"]
    control.release_online(service)
    return jsonify({"status": True, "data": "success"})

# dms_job.append({"func": "%s:system_auto_release" % __name__, "trigger": "cron", "id": "release_ih_daily",
#                 "day_of_week": "0-4", "hour": "12", "minute": "10"})
