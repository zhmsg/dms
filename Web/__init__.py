# encoding: utf-8
# !/usr/bin/python

from flask import Flask
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
    return user


login_manager.login_view = "transport_view.index"


