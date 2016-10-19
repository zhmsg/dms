#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import tornado.web
from Web2 import make_static_html


class StaticModule(tornado.web.UIModule):

    def render(self, file_path):
        return make_static_html(file_path)
