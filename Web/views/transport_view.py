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

transport_view = Blueprint('transport_view', __name__)

my_email = MyEmailManager()
user_m = UserManager()
control = ControlManager()


@transport_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


@transport_view.route("/", methods=["GET"])
def index():
    return render_template("login.html")


@transport_view.route("/login/", methods=["POST"])
def login():
    request_data = request.form
    user_name = request_data["user_name"]
    password = request_data["password"]
    result, message = user_m.check(user_name, password)
    if result is False:
        return message
    user = User()
    user.account = user_name
    login_user(user)
    session["role"] = message
    return redirect(url_for("transport_view.show"))


@transport_view.route("/records/", methods=["GET"])
@login_required
def show():
    try:
        data_info = control.get_data()
        return render_template("infoShow.html", data_info=data_info, user_name=current_user.account, role=session["role"],
                               market_target=control.market_target, market_attribute=control.market_attribute,
                               market_attribute_ch=control.market_attribute_ch, upload_attribute=control.upload_attribute,
                               upload_attribute_ch=control.upload_attribute_ch, calc_attribute=control.calc_attribute,
                               calc_attribute_ch=control.calc_attribute_ch)
    except Exception as e:
        error_message = u"获得记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/data/", methods=["POST"])
@login_required
def new_data():
    try:
        result, message = control.new_data(session["role"], current_user.account)
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/market/", methods=["POST"])
@login_required
def new_market():
    try:
        request_data = request.form
        data_no = request_data["data_no"]
        market_info = {}
        for att in control.market_attribute:
            market_info[att] = request_data[att]
        result, message = control.new_market(data_no, market_info, current_user.account, session["role"])
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/upload/", methods=["POST"])
@login_required
def new_upload():
    try:
        request_data = request.form
        data_no = request_data["data_no"]
        upload_info = {}
        for att in control.upload_attribute:
            upload_info[att] = request_data[att]
        result, message = control.new_upload(data_no, upload_info, current_user.account, session["role"])
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/calc/", methods=["POST"])
@login_required
def new_calc():
    try:
        request_data = request.form
        data_no = request_data["data_no"]
        calc_info = {}
        for att in control.calc_attribute:
            calc_info[att] = request_data[att]
        result, message = control.new_calc(data_no, calc_info, current_user.account, session["role"])
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message