# encoding: utf-8
# !/usr/bin/python

from flask import session
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

data_dir = "/data/dms"

import os

if os.path.isdir(data_dir) is False:
    os.mkdir(data_dir)
