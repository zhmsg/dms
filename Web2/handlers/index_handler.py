#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import tornado.web
from Web2 import http_handlers, ado_prefix, dms_url_prefix

url_prefix = ado_prefix + dms_url_prefix


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("login.html")


http_handlers.append((url_prefix + "/", IndexHandler))