# encoding: utf-8
# !/usr/bin/python

from datetime import datetime
from functools import wraps
from flask import session, g, make_response, Blueprint, jsonify, request
from flask_login import LoginManager, UserMixin, login_required
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events
from Tools.Mysql_db import DB
from Tools.MyEmail import MyEmailManager
from Class.Control import ControlManager
from Function.Common import *


__author__ = 'zhouheng'

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

db = DB()
ip = IPManager()
control = ControlManager()
my_email = MyEmailManager("/home/msg/conf/")
dms_scheduler = BackgroundScheduler()
# job_store = SQLAlchemyJobStore(url=db.url)
# dms_scheduler.add_jobstore(job_store)


def err_listener(ev):
    with open("dms_task.log", "a") as wr:
        wr.write("----------%s----------\n" % datetime.now().strftime(TIME_FORMAT))
        if isinstance(ev, apscheduler.events.JobSubmissionEvent):
            wr.write("Job Submission Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("job_id: %s\n" % ev.job_id)
            wr.write("scheduled_run_times: %s\n" % ev.scheduled_run_times)
        elif isinstance(ev, apscheduler.events.JobExecutionEvent):
            wr.write("Job Execution Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("job_id: %s\n" % ev.job_id)
            wr.write("scheduled_run_time: %s\n" % ev.scheduled_run_time)
            print(ev.scheduled_run_time)
            wr.write("retval: %s\n" % ev.retval)
            wr.write("exception: %s\n" % ev.exception)
            wr.write("traceback: %s\n" % ev.traceback)
        elif isinstance(ev, apscheduler.events.JobEvent):
            wr.write("Job Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("job_id: %s\n" % ev.job_id)
        elif isinstance(ev, apscheduler.events.SchedulerEvent):
            wr.write("Scheduler Event\n")
            wr.write("code: %s\n" % ev.code)
            wr.write("alias: %s\n" % ev.alias)
        wr.write("----------end----------\n")

dms_scheduler.add_listener(err_listener)


class User(UserMixin):
    user_name = ""

    def get_id(self):
        return self.user_name

login_manager = LoginManager()
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_name):
    user = User()
    user.user_name = user_name
    if "role" in session:
        user.role = session["role"]
    else:
        select_sql = "SELECT role FROM sys_user WHERE user_name='%s';" % user_name
        print(select_sql)
        result = db.execute(select_sql)
        if result > 0:
            user.role = db.fetchone()[0]
            session["role"] = user.role
        else:
            user.role = 0
            session["role"] = user.role
    return user


login_manager.login_view = "dms_view.index"
web_prefix = web_prefix_url
api_url_prefix = web_prefix + "/dev/api"
status_url_prefix = web_prefix + "/dev/api/status"
test_url_prefix = web_prefix + "/dev/api/test"
bug_url_prefix = web_prefix + "/dev/bug"
right_url_prefix = web_prefix + "/dev/right"
param_url_prefix = web_prefix + "/dev/param"
dev_url_prefix = web_prefix + "/dev"
dms_url_prefix = web_prefix + ""
data_url_prefix = web_prefix + "/data"
log_url_prefix = web_prefix + "/log"
tools_url_prefix = web_prefix + "/tools"
release_url_prefix = web_prefix + "/dev/release"
github_url_prefix = web_prefix + "/github"
chat_url_prefix = web_prefix + "/chat"
others_url_prefix = web_prefix + "/others"
pay_url_prefix = web_prefix + "/wx/pay"

data_dir = "/ossdata/dmsdata"

import os
if os.path.isdir(data_dir) is False:
    os.mkdir(data_dir)


def company_ip_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "request_IP" not in g:
            return make_response(u"因为一些原因页面丢失了", 404)
        if g.request_IP not in range(company_ips[0], company_ips[1]) and g.user_name != "zh_test":
            return make_response(u"因为一些原因页面不知道去哪了", 404)
        return f(*args, **kwargs)
    return decorated_function


blues = {}
dms_job = []


def create_blue(blue_name, url_prefix="/", auth_required=True):
    add_blue = Blueprint(blue_name, __name__)
    if auth_required:
        @add_blue.before_request
        @login_required
        def before_request():

            g.role_value = control.role_value

    @add_blue.route("/ping/", methods=["GET"])
    def ping():
        from time import sleep
        sleep(5)
        return jsonify({"status": True, "message": "ping %s success" % request.path})

    if blue_name not in blues:
        blues[blue_name] = [add_blue, url_prefix]
    return add_blue
