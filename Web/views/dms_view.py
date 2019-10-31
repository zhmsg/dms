#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from flask import request, render_template, redirect, session, url_for, jsonify, g, make_response, current_app
from flask.sessions import SecureCookieSessionInterface
from flask_login import login_user, current_user, logout_user
from flask_login import login_required
from werkzeug.security import gen_salt
from Class import mongo_host
from Class.User import RoleManager
from Web import User

from Web import dms_url_prefix, dev_url_prefix, api_url_prefix, bug_url_prefix, right_url_prefix
from Web import log_url_prefix, create_blue, param_url_prefix, release_url_prefix, status_url_prefix
from Web import jingdu_url_prefix, dyups_url_prefix
from Web import control

from dms.objects.user import UserObject

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = dms_url_prefix

dms_view = create_blue('dms_view', url_prefix=url_prefix, auth_required=False)


user_m = UserObject()
role_m = RoleManager(mongo_host)


def load_domain_session():
    session_interface = SecureCookieSessionInterface()
    o_session = session_interface.open_session(current_app, request)
    return o_session


@dms_view.route("/", methods=["GET", "PUT", "POST", "DELETE"])
def index():
    next_url = ""
    if current_user.is_authenticated:
        if current_user.role == 0:
            return u"您还没有任何权限，请联系管理员授权"
        else:
            return redirect(url_prefix + "/portal/")
    if g.accept_json or request.headers.get("X-Requested-With") == "XMLHttpRequest" or \
            request.args.get("rf") == "rsync":
        return make_response("登录状态已过期，需要重新登录", 302)
    if "next" in request.args:
        next_url = request.args["next"]
    o_session = load_domain_session()
    if "user_id" in o_session and "auth_password" in o_session:
        domain_user = o_session["user_id"]
    else:
        domain_user = None
    return render_template("login.html", next_url=next_url, url_prefix=url_prefix, domain_user=domain_user)


@dms_view.route("/login/", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        logout_user()
    return index()


@dms_view.route("/login/", methods=["POST"])
def login():
    request_data = request.json
    if "domain_user" in request_data:
        o_session = load_domain_session()
        if "auth_password" not in o_session or "user_id" not in o_session:
            return jsonify({"status": False, "data": "登录失败"})
        user_name = o_session["user_id"]
        password = o_session["auth_password"]
    else:
        user_name = request_data["user_name"]
        password = request_data["password"]
    r_code, info = user_m.user_confirm(password, user=user_name)
    if r_code == -3:
        return jsonify({"status": False, "data": "内部错误"})
    elif r_code == -2:
        return jsonify({"status": False, "data": "账号不存在"})
    elif r_code == -1:
        return jsonify({"status": False, "data": "密码不正确"})
    session["role"] = info["role"]
    session["roles"] = dict()  # role_m.select(info["account"])
    # if info["tel"] is None:
    #     session["user_name"] = info["user_name"]
    #     session["bind_token"] = gen_salt(57)
    #     session["expires_in"] = datetime.now() + timedelta(seconds=300)
    #     session["password"] = password
    #     return jsonify({"status": True, "data": {"location": "%s/tel/" % url_prefix, "user_name": info["user_name"]}})
    if "remember" in request_data and request_data["remember"] == "on":
        remember = True
    else:
        remember = False
    user = User()
    user.user_name = info["user_name"]
    login_user(user, remember=False)
    if "next" in request_data and request_data["next"] != "":
        return jsonify({"status": True, "data": {"location": request_data["next"], "user_name": user.user_name}})
    if session["role"] == 0:
        return jsonify({"status": False, "data": "您还没有任何权限，请联系管理员授权"})
    else:
        return jsonify({"status": True, "data": {"location": url_prefix + "/portal/", "user_name": user.user_name}})


@dms_view.route("/login/vip/", methods=["POST"])
def login_vip():
    request_data = request.json
    user_name = request_data["user_name"]
    result, info = user_m.check_vip(user_name)
    if result is False:
        return jsonify({"status": False, "data": "fail"})
    user = User()
    user.user_name = info["account"]
    login_user(user)
    session["role"] = info["role"]
    session["roles"] = role_m.select(info["account"])
    session.modified = True
    return jsonify({"status": True, "data": "success"})


@dms_view.route("/password/", methods=["GET"])
def password_page():
    if "user_name" in g:
        return render_template("password.html", url_prefix=url_prefix)
    elif "change_token" in session and "expires_in" in session and "user_name" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            return render_template("password.html", user_name=session["user_name"],
                                   change_token=session["change_token"], url_prefix=url_prefix)
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/tel/", methods=["GET"])
def bind_tel_page():
    if "bind_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            return render_template("tel.html", user_name=session["user_name"],
                                   bind_token=session["bind_token"], url_prefix=url_prefix)
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/tel/", methods=["PUT"])
def send_tel_code():
    if "bind_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            request_data = request.json
            bind_token = request_data["bind_token"]
            if bind_token != session["bind_token"]:
                return redirect(url_for("dms_view.login_page"))
            tel = request_data["tel"]
            result, info = control.send_code(session["user_name"], session["password"], tel)
            if result is True:
                session["tel"] = tel
                return jsonify({"status": True, "data": {"tel": tel}})
            return jsonify({"status": False, "data": info})
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/tel/", methods=["POST"])
def bind_tel_func():
    if "bind_token" in session and "expires_in" in session and "user_name" in session and "password" in session:
        expires_in = session["expires_in"]
        if expires_in > datetime.now():
            if "tel" not in session:
                return jsonify({"status": False, "data": "Please Send Code"})
            request_data = request.json
            bind_token = request_data["bind_token"]
            if bind_token != session["bind_token"]:
                return redirect(url_for("dms_view.login_page"))
            tel = request_data["tel"]
            if tel != session["tel"]:
                return jsonify({"status": False, "data": "Please Send Code First"})
            code = request_data["code"]
            user_name = session["user_name"]
            result, info = control.bind_tel(user_name, session["password"], tel, code)
            if result is True:
                user = User()
                user.user_name = user_name
                login_user(user)
                del session["bind_token"]
                del session["expires_in"]
                del session["user_name"]
                del session["password"]
                del session["tel"]
                return jsonify({"status": True, "data": {"tel": tel}})
            else:
                return jsonify({"status": False, "data": info})
    return redirect(url_for("dms_view.login_page"))


@dms_view.route("/password/", methods=["POST"])
def set_password():
    user_name = request.form["user_name"]
    new_password= request.form["new_password"]
    confirm_password = request.form["confirm_password"]
    if new_password != confirm_password:
        return "两次输入密码不一致"
    if current_user.is_authenticated:
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
    if g.user_role & control.role_value["user_new"] <= 0:
        return u"用户无权限操作"
    check_url = url_prefix + "/register/check/"
    return render_template("register.html", url_prefix=url_prefix, check_url=check_url, role_desc=control.user.role_desc)


@dms_view.route("/register/", methods=["POST"])
@login_required
def register():
    request_data = request.form
    user_name = request_data["user_name"]
    if "register_name" not in session or session["register_name"] != user_name:
        return u"页面已过期，请刷新重试"
    nick_name = request_data["nick_name"]
    user_role = 0
    for key, role_module in control.user.role_desc.items():
        for role_key, role_info in role_module["role_list"].items():
            if role_key in request.form and request.form[role_key] == "on":
                user_role += role_info["role_value"]
    result, message = control.new_user(user_name, user_role, nick_name, current_user.user_name, current_user.role)
    if result is False:
        return message
    return redirect(url_for("dms_view.select_portal"))


@dms_view.route("/register/check/", methods=["POST"])
@login_required
def register_check():
    request_data = request.json
    check_name = request_data["check_name"]
    result, message = control.check_user_name_exist(current_user.user_name, current_user.role, check_name)
    if result is True:
        session["register_name"] = message
    return jsonify({"status": True, "data": {"result": result, "message": message}})


@dms_view.route("/remove/user/", methods=["DELETE"])
@login_required
def remove_register_user():
    user_name = request.json["user_name"]
    user_m.remove_user(user_name, g.user_name)
    return jsonify({"status": True, "data": "success"})


@dms_view.route("/authorize/", methods=["GET"])
@login_required
def authorize_page():
    result, my_user = control.get_my_user(current_user.user_name, current_user.role)
    if result is False:
        return my_user
    url_remove = url_prefix + "/remove/user/"
    return render_template("authorize.html", my_user=my_user, url_prefix=url_prefix,
                           role_desc=control.user.role_desc, url_remove=url_remove)


@dms_view.route("/authorize/user/", methods=["POST"])
@login_required
def authorize():
    perm_user = request.form["perm_user"]
    if perm_user == "":
        return "请选择一个账户"
    user_role = 0
    for key, role_module in control.user.role_desc.items():
        for role_key, role_info in role_module["role_list"].items():
            if role_key in request.form and request.form[role_key] == "on":
                user_role += role_info["role_value"]
    result, message = control.update_my_user_role(current_user.role, current_user.user_name, perm_user, user_role)
    if result is False:
        return message
    return redirect(url_for("dms_view.authorize_page"))


@dms_view.route("/portal/", methods=["GET"])
@login_required
def select_portal():
    menu = [
        {"desc": u"API文档", "url": api_url_prefix}
    ]
    return render_template("portal.html", menu=menu, dev_url_prefix=dev_url_prefix,
                           bug_url_prefix=bug_url_prefix,
                           dms_url_prefix=dms_url_prefix, right_url_prefix=right_url_prefix,
                           log_url_prefix=log_url_prefix, param_url_prefix=param_url_prefix,
                           release_url_prefix=release_url_prefix, status_url_prefix=status_url_prefix,
                           jd_url_prefix=jingdu_url_prefix, dyups_url_prefix=dyups_url_prefix)


@dms_view.route("/user/", methods=["GET"])
@login_required
def list_user():
    items = user_m.list_user(g.user_name)
    return jsonify({"status": True, "data": items})


@dms_view.route("/policies", methods=["GET"])
@login_required
def get_policies():
    role = session["role"]
    policies = dict(api_help=["api_module_new", "api_new", "api_look"])
    return jsonify({"status": True, "data": {"role": role,
                                             "policies": policies}})
