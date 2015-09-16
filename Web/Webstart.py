#! /usr/bin/env python
# coding: utf-8
import sys
sys.path.append("..")
from flask import Flask
from Web.views import transport_view as transport_view_blueprint
from Web import login_manager

__author__ = 'zhouheng'

msg_web = Flask("__name__")
msg_web.secret_key = 'meisanggou'
login_manager.init_app(msg_web)
msg_web.register_blueprint(transport_view_blueprint, url_prefix="/dms")


if __name__ == '__main__':
    msg_web.run(host="0.0.0.0", port=2100)
