# encoding: utf-8
# !/usr/bin/python

from flask import g, request
from flask_helper.flask_hook import FlaskHook


__author__ = 'zhouhenglc'


class AcceptHook(FlaskHook):
    priority = 110

    def before_request(self):
        if "Accept" in request.headers and request.headers["Accept"].find("application/json") >= 0:
            g.accept_json = True
        else:
            g.accept_json = False
