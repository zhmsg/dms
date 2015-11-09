#!/user/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
from flask import Blueprint, request, render_template, redirect, session, url_for
from flask_login import login_user, current_user
from Tools.MyEmail import MyEmailManager
from flask_login import login_required
from Class.User import UserManager
from Class.Control import ControlManager
from Web import User

sys.path.append('..')

__author__ = 'Zhouheng'

my_email = MyEmailManager()

dms_view = Blueprint('dms_view', __name__, url_prefix="/dms")


user_m = UserManager()
control = ControlManager()


@dms_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@dms_view.route("/", methods=["GET"])
def index():
    next_url = ""
    if current_user.is_authenticated():
        if current_user.role == 0:
            return u"您还没有任何权限，请联系管理员授权"
        elif current_user.role < 8:
            return redirect(url_for("transport_view.show"))
        elif current_user.role < 32:
            return redirect(url_for("develop_api_view.list_api"))
        elif current_user.role < 64:
            return redirect(url_for("develop_view.show_data_table"))
        else:
            return redirect(url_for("develop_view.operate_auth_show"))
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url)


@dms_view.route("/login/", methods=["GET"])
def login_page():
    next_url = ""
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url)


@dms_view.route("/register/", methods=["GET"])
def register_page():
    return render_template("register.html")


@dms_view.route("/register/", methods=["POST"])
def register():
    request_data = request.form
    user_name = request_data["user_name"]
    password = request_data["password"]
    result, message = user_m.new(user_name, password, 0, "")
    if result is False:
        return message
    return redirect(url_for("dms_view.login_page"))
