# encoding: utf-8
# !/usr/bin/python

from functools import wraps
from flask import session, g, make_response
from flask.ext.login import LoginManager, UserMixin
from Tools.Mysql_db import DB
from Tools.MyIP import IPManager
from Tools.MyEmail import MyEmailManager

__author__ = 'zhouheng'

db = None
try:
    db = DB()
except Exception, e:
    print e


class User(UserMixin):
    account = ""

    def get_id(self):
        return self.account

login_manager = LoginManager()
login_manager.session_protection = 'strong'

ip = IPManager()
my_email = MyEmailManager("/home/msg/conf/")


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
bug_url_prefix = "/dev/bug"
right_url_prefix = "/dev/right"
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
        env = r_env.read()

if env == "Development":
    company_ips = [3232266241, 3232266495]  # 192.168.120.1 -- 192.168.120.254
else:
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
