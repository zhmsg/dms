#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, redirect, session, url_for
from flask_login import login_user, current_user, logout_user
from flask_login import login_required
from werkzeug.security import gen_salt
from Class.User import UserManager
from Web import User

from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

dms_view = Blueprint('dms_view', __name__, url_prefix="/dms")


user_m = UserManager()


@dms_view.route("/ping/", methods=["GET"])
def ping():
    return "true"


def calc_redirect(role):
    if role >= 1 and role <= 7:
        url_for_fun = "transport_view.show"
    elif role == 8 or role == 16 or role == 24:
        url_for_fun = "develop_api_view.list_api"
    elif role == 32:
        url_for_fun = "develop_view.show_data_table"
    elif role == 64:
        url_for_fun = "develop_view.operate_auth_show"
    elif role == 128:
        url_for_fun = "dms_view.register_page"
    elif role == 256 or role == 256 + 512:
        url_for_fun = "develop_bug_view.show_bug_list"
    else:
        url_for_fun = "dms_view.select_portal"
    return url_for_fun


@dms_view.route("/", methods=["GET"])
def index():
    next_url = ""
    # if current_user.is_authenticated():
    #     if current_user.role == 0:
    #         return u"您还没有任何权限，请联系管理员授权"
    #     else:
    #         return redirect(url_for(calc_redirect(current_user.role)))
    # if "next" in request.args:
    #     next_url = request.args["next"]
    return render_template("login.html", next_url=next_url)


@dms_view.route("/login/", methods=["GET"])
def login_page():
    if current_user.is_authenticated():
        logout_user()
    next_url = ""
    if "next" in request.args:
        next_url = request.args["next"]
    return render_template("login.html", next_url=next_url)


@dms_view.route("/login/", methods=["POST"])
def login():
    request_data = request.form
    user_name = request_data["user_name"]
    password = request_data["password"]
    result, role = user_m.check(user_name, password)
    if result is False:
        return role
    if role == -1:
        session["user_name"] = user_name
        session["change_token"] = gen_salt(57)
        session["expires_in"] = datetime.now() + timedelta(seconds=300)
        session["password"] = password
        return redirect(url_for("dms_view.password_page"))
    if "remember" in request_data and request_data["remember"] == "on":
        remember = True
    else:
        remember = False
    user = User()
    user.account = user_name
    login_user(user, remember=remember)
    session["role"] = role
    if "next" in request_data and request_data["next"] != "":
        return redirect(request_data["next"])
    if session["role"] == 0:
            return u"您还没有任何权限，请联系管理员授权"
    else:
        return redirect(url_for(calc_redirect(session["role"])))


@dms_view.route("/password/", methods=["GET"])
def password_page():
    if current_user.is_authenticated():
        return render_template("password.html", user_name=current_user.account)
    elif "change_token" in session and "expires_in" in session and "user_name" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            return render_template("password.html", user_name=session["user_name"], change_token=session["change_token"])
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/password/", methods=["POST"])
def password():
    user_name = request.form["user_name"]
    new_password= request.form["new_password"]
    confirm_password = request.form["confirm_password"]
    if new_password != confirm_password:
        return "两次输入密码不一致"
    if current_user.is_authenticated():
        old_password= request.form["old_password"]
        if old_password == new_password:
            return u"新密码不能和旧密码一样"
        result, message = control.change_password(user_name, old_password, new_password)
        if result is False:
            return message
        return redirect(url_for("dms_view.login_page"))
    elif "change_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            change_token = request.form["change_token"]
            if change_token != session["change_token"]:
                return "Bad change_token"
            if user_name != session["user_name"]:
                return "Bad user_name"
            result, message = control.change_password(user_name, session["password"], new_password)
            if result is False:
                return message
            del session["user_name"]
            del session["change_token"]
            del session["expires_in"]
            del session["password"]
            return redirect(url_for("dms_view.login_page"))
        else:
            return "更新密码超时，请重新登录"
    return "更新失败，请重新登录"


@dms_view.route("/register/", methods=["GET"])
@login_required
def register_page():
    if current_user.role & control.user_role["user_new"] <= 0:
        return u"用户无权限操作"
    return render_template("register.html", user_role=current_user.role, role_value=control.user_role)


@dms_view.route("/register/", methods=["POST"])
@login_required
def register():
    request_data = request.form
    user_name = request_data["user_name"]
    nick_name = request_data["nick_name"]
    user_role = 0
    for key, value in control.user_role.items():
        if key in request_data and request_data[key] == "on":
            user_role += value
    result, message = control.new_user(user_name, user_role, nick_name, current_user.account, current_user.role)
    if result is False:
       return message
    return redirect(url_for("dms_view.select_portal"))


@dms_view.route("/authorize/", methods=["GET"])
@login_required
def authorize_page():
    result, my_user = control.get_my_user(current_user.account, current_user.role)
    if result is False:
        return my_user
    return render_template("authorize.html", my_user=my_user, user_role=current_user.role, role_value=control.user_role)


@dms_view.route("/authorize/user/", methods=["POST"])
@login_required
def authorize():
    perm_user = request.form["perm_user"]
    if perm_user == "":
        return "请选择一个账户"
    user_role = 0
    for key, value in control.user_role.items():
        if key in request.form and request.form[key] == "on":
            user_role += value
    result, message = control.update_my_user_role(current_user.role, current_user.account, perm_user, user_role)
    if result is False:
        return message
    return redirect(url_for("dms_view.authorize_page"))


@dms_view.route("/portal/", methods=["GET"])
@login_required
def select_portal():
    return render_template("portal.html", user_role=current_user.role, role_value=control.user_role)

