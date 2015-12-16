#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
from flask import Flask, request
from Web.views.transport_view import transport_view as transport_view_blueprint
from Web.views.develop_view import develop_view as develop_view_blueprint
from Web.views.develop_api_view import develop_api_view as develop_api_view_blueprint
from Web.views.dms_view import dms_view as dms_blueprint
from Web.views.develop_bug_view import develop_bug_view as bug_blueprint
from Web import login_manager, data_url_prefix, dev_url_prefix, api_url_prefix, dms_url_prefix, bug_url_prefix

__author__ = 'zhouheng'

msg_web = Flask("__name__")
msg_web.secret_key = 'meisanggou'
login_manager.init_app(msg_web)
msg_web.register_blueprint(transport_view_blueprint, url_prefix=data_url_prefix)
msg_web.register_blueprint(develop_view_blueprint, url_prefix=dev_url_prefix)
msg_web.register_blueprint(develop_api_view_blueprint, url_prefix=api_url_prefix)
msg_web.register_blueprint(dms_blueprint, url_prefix=dms_url_prefix)
msg_web.register_blueprint(bug_blueprint, url_prefix=bug_url_prefix)


@msg_web.template_filter('bit_and')
def bit_and(num1, num2):
    return num1 & num2

msg_web.jinja_env.filters['bit_and'] = bit_and


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


if __name__ == '__main__':
    print("start run")
    msg_web.run(host="0.0.0.0", port=2200)
