#!/user/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
from flask import Blueprint, request, render_template, redirect, session, url_for, send_from_directory
from flask_login import login_user, current_user
from Tools.MyEmail import MyEmailManager
from flask_login import login_required
from Class.User import UserManager
from Class.Control import ControlManager
from Web import User

sys.path.append('..')

__author__ = 'Zhouheng'

my_email = MyEmailManager()

develop_view = Blueprint('develop_view', __name__)

my_email = MyEmailManager()
user_m = UserManager()
control = ControlManager()


@develop_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@develop_view.route("/operate/auth/", methods=["GET"])
def operate_auth_show():
    result, data = control.show_operate_auth()
    if result is False:
        return data
    return render_template("/Dev/operate_auth.html", operate_auth=data)


@develop_view.route("/operate/auth/download/", methods=["GET"])
def download_operate_auth():
    result, data = control.download_operate_auth()
    print(data)
    if result is True:
        return send_from_directory(data["DIR"], data["FILE"], as_attachment=True)
    return data
