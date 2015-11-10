# encoding: utf-8
# !/usr/bin/python

from flask import session
from flask.ext.login import LoginManager, UserMixin
from Tools.Mysql_db import DB

__author__ = 'zhouheng'

db = None
try:
    db = DB()
    db.connect()
except Exception, e:
    print e


class User(UserMixin):
    account = ""

    def get_id(self):
        return self.account

login_manager = LoginManager()


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
    return user


login_manager.login_view = "dms_view.index"


