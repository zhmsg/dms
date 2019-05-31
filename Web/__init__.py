# encoding: utf-8
# !/usr/bin/python

from datetime import datetime
from redis import Redis
from functools import wraps
from flask import session, g, make_response, Blueprint, jsonify, request, redirect
from flask_login import LoginManager, UserMixin, login_required
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events
from Tools.Mysql_db import DB
from JYTools import EmailManager
from Class.Control import ControlManager
from Function.Common import *


__author__ = 'zhouheng'

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

db = DB()
ip = IPManager()
control = ControlManager()
my_email = EmailManager(conf_dir)
dms_scheduler = BackgroundScheduler()
redis = Redis(host=redis_host, port=redis_port)
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
# login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_name):
    user = User()
    user.user_name = user_name
    if "roles" in session:
        user.roles = session["roles"]
    else:
        user.roles = None
        session["roles"] = None
    if "role" in session:
        user.role = session["role"]
    else:
        user.role = 0
        session["role"] = user.role
    return user


login_manager.login_view = "dms_view.index"
web_prefix = web_prefix_url
api_url_prefix = web_prefix + "/dev/api"
status_url_prefix = web_prefix + "/dev/api/status"
test_url_prefix = web_prefix + "/dev/api/test"
bug_url_prefix = web_prefix + "/dev/problem"
right_url_prefix = web_prefix + "/dev/right"
param_url_prefix = web_prefix + "/dev/param"
dev_url_prefix = web_prefix + "/dev"
dms_url_prefix = web_prefix + ""
data_url_prefix = web_prefix + "/data"
log_url_prefix = web_prefix + "/log"
tools_url_prefix = web_prefix + "/tools"
release_url_prefix = web_prefix + "/dev/release"
dyups_url_prefix = web_prefix + "/dev/dyups"
github_url_prefix = web_prefix + "/github"
chat_url_prefix = web_prefix + "/chat"
others_url_prefix = web_prefix + "/others"
pay_url_prefix = web_prefix + "/wx/pay"
jingdu_url_prefix = web_prefix + "/jd"
editor_url_prefix = web_prefix + "/editor"
article_url_prefix = web_prefix + "/article"
message_url_prefix = web_prefix + "/message"
short_link_prefix = web_prefix + "/s"
dist_key_prefix = web_prefix + "/dist/key"
performance_prefix = web_prefix + "/performance"

data_dir = "/geneac/dmsdata"

editor_data_dir = data_dir + "/editor"
article_data_dir = data_dir + "/article"

if os.path.isdir(article_data_dir) is False:
    os.mkdir(article_data_dir)

import os
if os.path.isdir(data_dir) is False:
    os.mkdir(data_dir)

if os.path.isdir(editor_data_dir) is False:
    os.mkdir(editor_data_dir)


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


def create_blue(blue_name, url_prefix="/", auth_required=True, special_protocol=False):
    add_blue = Blueprint(blue_name, __name__)
    if auth_required:
        @add_blue.before_request
        @login_required
        def before_request():
            if special_protocol is True:
                r_protocol = request.headers.get("X-Request-Protocol", "http")
                if r_protocol not in request_special_protocol:
                    redirect_url = "%s://%s%s" % (request_special_protocol[0], request.host, request.full_path)
                    return redirect(redirect_url)

            g.role_value = control.role_value

    @add_blue.route("/ping/", methods=["GET"])
    def ping():
        from time import sleep
        sleep(5)
        return jsonify({"status": True, "message": "ping %s success" % request.path})

    if blue_name not in blues:
        blues[blue_name] = [add_blue, url_prefix]
    return add_blue


    # @login_manager.unauthorized_callback
    # def unauthorized_callback_func():
    #     if request.is_xhr:
    #         return make_response("登录状态已过期，需要重新登录", 302)