#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
import os
import re
from flask import Flask, request, make_response, g, jsonify
from flask_login import current_user
from Web import login_manager, unix_timestamp, bit_and, current_env, ip_str, make_static_url, make_default_static_url
from Web import ip, dms_scheduler, user_blacklist, cookie_domain, dms_job, make_static_html, control
from redis_session import RedisSessionInterface

__author__ = 'zhouheng'

accept_agent = "(firefox|chrome|safari|window|GitHub|jyrequests)"
trust_proxy = ["127.0.0.1", "10.25.244.32", "10.44.147.192"]


def create_app():
    msg_web = Flask("__name__")
    msg_web.secret_key = 'meisanggou'
    login_manager.init_app(msg_web)

    @msg_web.before_request
    def before_request():
        request_ip = request.remote_addr
        if "X-Forwarded-For" in request.headers:
            if request.remote_addr in trust_proxy:
                request_ip = request.headers["X-Forwarded-For"].split(",")[0]
        g.request_IP_s = request_ip
        g.request_IP = ip.ip_value_str(ip_str=request_ip)
        if g.request_IP == 0:
            return make_response(u"IP受限", 403)
        if "User-Agent" not in request.headers:
            print("No User-Agent")
            return make_response(u"请使用浏览器访问", 403)
        user_agent = request.headers["User-Agent"]
        if re.search(accept_agent, user_agent, re.I) is None:
            return make_response(u"浏览器版本过低", 403)
        if current_user.is_authenticated:
            g.user_role = current_user.role
            g.user_name = current_user.account
            if g.user_name in user_blacklist:
                message =u"不好意思，您的帐号存在异常，可能访问本系统出现不稳定的想象，现在就是不稳定中。本系统不是很智能，所以不知道啥时候会稳定，也许一分钟，也许一天，也许。。。"
                if "X-Requested-With" in request.headers:
                    return jsonify({"status": False, "data": message})
                return message
        else:
            g.user_role = 0

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
        res.headers["Server"] = "JingYun Server"
        return res

    @msg_web.errorhandler(500)
    def handle_500(e):
        return str(e)

    msg_web.session_interface = RedisSessionInterface()

    msg_web.static_folder = "static2"
    msg_web.session_cookie_name = "jydms"
    if cookie_domain != "":
        msg_web.config.update(SESSION_COOKIE_DOMAIN=cookie_domain)
    msg_web.config.update(PERMANENT_SESSION_LIFETIME=600)

    api_files = os.listdir("./views")
    for api_file in api_files:
        if api_file.endswith("_view.py"):
            __import__("Web.views.%s" % api_file[:-3])

    from Web import blues
    for key, value in blues.items():
        if len(value[1]) > 1:
            msg_web.register_blueprint(value[0], url_prefix=value[1])
        else:
            msg_web.register_blueprint(value[0])

    env = msg_web.jinja_env
    env.globals["current_env"] = current_env
    env.globals["role_value"] = control.role_value
    env.filters['unix_timestamp'] = unix_timestamp
    env.filters['bit_and'] = bit_and
    env.filters['ip_str'] = ip_str
    env.filters['make_static_url'] = make_static_url
    env.filters['make_default_static_url'] = make_default_static_url
    env.filters['make_static_html'] = make_static_html
    return msg_web

msg_web = create_app()

for item in dms_job:
    item["max_instances"] = 10
    item["replace_existing"] = True
    dms_scheduler.add_job(**item)
dms_scheduler.start()


if __name__ == '__main__':
    print("start run")
    msg_web.run(port=2200)
