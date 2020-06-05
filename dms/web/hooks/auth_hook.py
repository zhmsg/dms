# encoding: utf-8
# !/usr/bin/python

from flask import g, request
from flask_login import current_user

from dms.web import FlaskHook


__author__ = 'zhouhenglc'


class AuthHook(FlaskHook):
    priority = 110

    def before_request(self):
        if current_user.is_authenticated:
            g.user_role = current_user.role
            g.user_name = current_user.user_name
            g.user_policies = current_user.policies
            # if g.user_name in user_blacklist:
            #     message ="不好意思，您的帐号存在异常，可能访问本系统出现不稳定的想象，现在就是不稳定中。本系统不是很智能，所以不知道啥时候会稳定，也许一分钟，也许一天，也许。。。"
            #     if "X-Requested-With" in request.headers:
            #         return jsonify({"status": False, "data": message})
            #     return message
        else:
            g.user_role = 0
