# encoding: utf-8
# !/usr/bin/python

import time
import ConfigParser
from functools import wraps
from flask import session, g, make_response, Blueprint, jsonify, request
from flask_login import LoginManager, UserMixin, login_required
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from Tools.Mysql_db import DB
from Tools.MyIP import IPManager
from Tools.MyEmail import MyEmailManager
from Class.Control import ControlManager


__author__ = 'zhouheng'

db = DB()
control = ControlManager()
ip = IPManager()
my_email = MyEmailManager("/home/msg/conf/")
dms_scheduler = BackgroundScheduler()
# job_store = SQLAlchemyJobStore(url=db.url)
# dms_scheduler.add_jobstore(job_store)


class User(UserMixin):
    account = ""

    def get_id(self):
        return self.account

login_manager = LoginManager()
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(account):
    user = User()
    user.account = account
    if "role" in session:
        user.role = session["role"]
    else:
        select_sql = "SELECT role FROM sys_user WHERE user_name='%s';" % account
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

api_url_prefix = "/dev/api"
status_url_prefix = "/dev/api/status"
test_url_prefix = "/dev/api/test"
bug_url_prefix = "/dev/bug"
right_url_prefix = "/dev/right"
param_url_prefix = "/dev/param"
dev_url_prefix = "/dev"
dms_url_prefix = ""
data_url_prefix = "/data"
log_url_prefix = "/log"
tools_url_prefix = "/tools"
release_url_prefix = "/dev/release"
github_url_prefix = "/github"

data_dir = "/ossdata/dmsdata"

import os

if os.path.exists("../env.conf") is False:
    env = "Development"

else:
    with open("../env.conf") as r_env:
        env = r_env.read().strip()

# read config
config = ConfigParser.ConfigParser()
config.read("../config.conf")

static_prefix_url = config.get(env, "static_prefix_url")
company_ip_start = config.getint(env, "company_ip_start")
company_ip_end = config.getint(env, "company_ip_end")
company_ips = [company_ip_start, company_ip_end]
cookie_domain = config.get(env, "cookie_domain")

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
user_blacklist = []
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
        return jsonify({"status": True, "message": "ping %s success" % request.path})

    if blue_name not in blues:
        blues[blue_name] = [add_blue, url_prefix]
    return add_blue


def unix_timestamp(t, style="time"):
    if type(t) == int or type(t) == long:
        x = time.localtime(t)
        if style == "time":
            return time.strftime('%H:%M:%S', x)
        else:
            return time.strftime("%Y-%m-%d %H:%M:%S", x)
    return t


def bit_and(num1, num2):
    return num1 & num2


def current_env(s):
    return env


def ip_str(ip_v):
    if type(ip_v) == int or type(ip_v) == long:
        return ip.ip_value_str(ip_value=ip_v)
    return ip_v


def make_static_url(filename):
    return static_prefix_url + "/" + filename


def make_default_static_url(filename):
    return static_prefix_url + "/" + filename


def make_static_html(filename):
    src = make_static_url(filename)
    default_src = make_default_static_url(filename)
    if filename.endswith(".js"):
        html_s = "<script type=\"text/javascript\" src=\"%s\" onerror=\"this.src='%s'\"></script>" % (src, default_src)
    else:
        html_s = "<link rel=\"stylesheet\" href=\"%s\" onerror=\"this.href='%s'\">" % (src, default_src)
    return html_s
