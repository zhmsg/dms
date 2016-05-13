#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
import time
import re
from flask import Flask, request, make_response
from Tools.MyIP import IPManager
from Web.views.transport_view import transport_view as transport_view_blueprint
from Web.views.develop_view import develop_view as develop_view_blueprint
from Web.views.develop_api_view import develop_api_view as develop_api_view_blueprint
from Web.views.develop_status_view import develop_status_view as develop_status_view_blueprint
from Web.views.dms_view import dms_view as dms_blueprint
from Web.views.develop_bug_view import develop_bug_view as bug_blueprint
from Web.views.develop_right_view import develop_right_view as right_blueprint
from Web.views.jy_log_view import jy_log_view as log_blueprint
from Web import login_manager, data_url_prefix, dev_url_prefix, api_url_prefix, dms_url_prefix, bug_url_prefix
from Web import right_url_prefix, log_url_prefix, status_url_prefix

__author__ = 'zhouheng'

msg_web = Flask("__name__")
msg_web.secret_key = 'meisanggou'
login_manager.init_app(msg_web)
msg_web.register_blueprint(transport_view_blueprint, url_prefix=data_url_prefix)
msg_web.register_blueprint(develop_view_blueprint, url_prefix=dev_url_prefix)
msg_web.register_blueprint(develop_api_view_blueprint, url_prefix=api_url_prefix)
msg_web.register_blueprint(develop_status_view_blueprint, url_prefix=status_url_prefix)
msg_web.register_blueprint(dms_blueprint, url_prefix=dms_url_prefix)
msg_web.register_blueprint(bug_blueprint, url_prefix=bug_url_prefix)
msg_web.register_blueprint(right_blueprint, url_prefix=right_url_prefix)
msg_web.register_blueprint(log_blueprint, url_prefix=log_url_prefix)


@msg_web.template_filter('bit_and')
def bit_and(num1, num2):
    return num1 & num2


@msg_web.template_filter('unix_timestamp')
def unix_timestamp(t):
    if type(t) == int or type(t) == long:
        x = time.localtime(t)
        return time.strftime('%H:%M:%S', x)
    return t

ip = IPManager()

accept_agent = "(firefox|chrome|safari)"


@msg_web.template_filter("ip_str")
def ip_str(ip_v):
    if type(ip_v) == int or type(ip_v) == long:
        return ip.ip_value_str(ip_value=ip_v)
    return ip_v


@msg_web.before_request
def before_request():
    if "User-Agent" not in request.headers:
        print("No User-Agent")
        return make_response(u"请使用浏览器访问", 403)
    user_agent = request.headers["User-Agent"]
    if re.search(accept_agent, user_agent, re.I) is None:
        return make_response(u"浏览器版本过低", 403)
    if "Referer" in request.headers:
        referer = request.headers["Referer"]
        print(referer)


@msg_web.after_request
def after_request(res):
    if res.status_code == 302 or res.status_code == 301:
        if "X-Request-Protocol" in request.headers:
            pro = request.headers["X-Request-Protocol"]
            if "Location" in res.headers:
                location = res.headers["location"]
                if location.startswith("http"):
                    res.headers["Location"] = res.headers["Location"].replace("http", pro)
                else:
                    res.headers["Location"] = "%s://%s%s" % (pro, request.headers["Host"], location)
    return res


# @msg_web.teardown_request
# def teardown_request(e=None):
#     print("enter teardown request")
msg_web.static_folder = "static2"

if __name__ == '__main__':
    print("start run")
    msg_web.run(host="0.0.0.0", port=2200)
