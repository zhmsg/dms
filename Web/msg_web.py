#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
from flask import Flask
from Web.views.transport_view import transport_view as transport_view_blueprint
from Web.views.develop_view import develop_view as develop_view_blueprint
from Web.views.develop_api_view import develop_api_view as develop_api_view_blueprint
from Web.views.dms_view import dms_view as dms_blueprint
from Web.views.develop_bug_view import develop_bug_view as bug_blueprint
from Web import login_manager

__author__ = 'zhouheng'

msg_web = Flask("__name__")
msg_web.secret_key = 'meisanggou'
login_manager.init_app(msg_web)
msg_web.register_blueprint(transport_view_blueprint, url_prefix="/dms")
msg_web.register_blueprint(develop_view_blueprint, url_prefix="/dev")
msg_web.register_blueprint(develop_api_view_blueprint)
msg_web.register_blueprint(dms_blueprint)
msg_web.register_blueprint(bug_blueprint)


@msg_web.template_filter('bit_and')
def bit_and(num1, num2):
    return num1 & num2

msg_web.jinja_env.filters['bit_and'] = bit_and


if __name__ == '__main__':
    print("start run")
    msg_web.run(host="0.0.0.0", port=2100)
