#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
from flask import Flask
from flask_login import current_user
from Web import *
from Web.redis_session import RedisSessionInterface

__author__ = 'zhouheng'


def create_app():
    msg_web = Flask(__name__)
    msg_web.secret_key = 'a string'
    login_manager.init_app(msg_web)

    @msg_web.before_request
    def before_request():
        test_r, info = normal_request_detection(request.headers, request.remote_addr)
        if test_r is False:
            return make_response(info, 403)
        g.request_IP_s, g.request_IP = info
        if current_user.is_authenticated:
            g.user_role = current_user.role
            g.user_name = current_user.user_name
            g.user_policies = current_user.policies
            if g.user_name in user_blacklist:
                message ="不好意思，您的帐号存在异常，可能访问本系统出现不稳定的想象，现在就是不稳定中。本系统不是很智能，所以不知道啥时候会稳定，也许一分钟，也许一天，也许。。。"
                if "X-Requested-With" in request.headers:
                    return jsonify({"status": False, "data": message})
                return message
        else:
            g.user_role = 0
        if "Accept" in request.headers and request.headers["Accept"].find("application/json") >= 0:
            g.accept_json = True
        else:
            g.accept_json = False

    @msg_web.after_request
    def after_request(res):
        if res.status_code == 302 or res.status_code == 301:
            if "X-Request-Protocol" in request.headers:
                pro = request.headers["X-Request-Protocol"]
                if "Location" in res.headers:
                    location = res.headers["location"]
                    if location.startswith("http:"):
                        res.headers["Location"] = pro + ":" + res.headers["Location"][5:]
                    elif location.startswith("/"):
                        res.headers["Location"] = "%s://%s%s" % (pro, request.headers["Host"], location)
        if "download_file" in g:
            try:
                os.system("rm -rf %s" % g.download_file)
            except Exception as e:
                print(e)
        res.headers["Server"] = "DMS Server"
        return res

    @msg_web.errorhandler(500)
    def handle_500(e):
        return str(e)

    # msg_web.session_interface = RedisSessionInterface(redis=redis, prefix=session_id_prefix,
    #                                                   cookie_name=session_cookie_name)

    msg_web.static_folder = "static2"
    if static_prefix_url.startswith("/"):
        msg_web.add_url_rule(static_prefix_url + '/<path:filename>', endpoint='static2',
                             view_func=msg_web.send_static_file)
    if cookie_domain != "":
        msg_web.config.update(SESSION_COOKIE_DOMAIN=cookie_domain)
    msg_web.config.update(PERMANENT_SESSION_LIFETIME=3000)

    api_files = os.listdir("./views")
    for api_file in api_files:
        if api_file not in ["develop_api_view.py", "dms_view.py",
                            'dms_config_view.py',
                            "develop_test_view.py", "short_link_view.py",
                            "develop_param_view.py", 'dms_user_policies_view.py']:
            continue
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
    env.globals["menu_url"] = dms_url_prefix + "/portal/"
    env.globals["short_link_url"] = short_link_prefix
    env.filters['unix_timestamp'] = unix_timestamp
    env.filters['bit_and'] = bit_and
    env.filters['ip_str'] = ip_str
    env.filters['make_static_url'] = make_static_url
    env.filters['make_default_static_url'] = make_default_static_url
    env.filters['make_static_html'] = make_static_html
    env.variable_start_string = "{{ "
    env.variable_end_string = " }}"
    return msg_web


msg_web = create_app()


if __name__ == '__main__':
    print("start run ")
    msg_web.run(port=2200)
