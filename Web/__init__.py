# encoding: utf-8
# !/usr/bin/python

import time
from functools import wraps
from flask import session, g, make_response, Blueprint, jsonify,request
from flask_login import LoginManager, UserMixin, login_required
from flask_apscheduler import APScheduler
from Tools.Mysql_db import DB
from Tools.MyIP import IPManager
from Tools.MyEmail import MyEmailManager

__author__ = 'zhouheng'

db = DB()
ip = IPManager()
my_email = MyEmailManager("/home/msg/conf/")
dms_scheduler = APScheduler()


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

data_dir = "/ossdata/dmsdata"

import os

if os.path.exists("../env.conf") is False:
    env = "Development"

else:
    with open("../env.conf") as r_env:
        env = r_env.read().strip()

if env == "Development":
    static_prefix_url = "/static"
    company_ips = [3232266241, 3232266495]  # 192.168.120.1 -- 192.168.120.254
else:
    static_prefix_url = "http://static.gene.ac/dms_static"
    company_ips = [2064103023, 2064103024]  # 123.7.182.111


if os.path.isdir(data_dir) is False:
    os.mkdir(data_dir)


def company_ip_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "request_IP" not in g:
            return make_response(u"因为一些原因页面丢失了", 404)
        if g.request_IP not in range(company_ips[0], company_ips[1]):
            return make_response(u"因为一些原因页面不知道去哪了", 404)
        return f(*args, **kwargs)
    return decorated_function


blues = {}


def create_blue(blue_name, url_prefix="/", auth_required=True):
    add_blue = Blueprint(blue_name, __name__)
    if auth_required:
        @add_blue.before_request
        @login_required
        def before_request():
                pass

    @add_blue.route("/ping/", methods=["GET"])
    def ping():
        return jsonify({"status": True, "message": "ping %s success" % request.path})

    if blue_name not in blues:
        blues[blue_name] = [add_blue, url_prefix]
    return add_blue


def unix_timestamp(t):
    if type(t) == int or type(t) == long:
        x = time.localtime(t)
        return time.strftime('%H:%M:%S', x)
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
