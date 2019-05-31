#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import json
import os
import sys
sys.path.append("..")
import tornado.web
import tornado.ioloop
import tornado.websocket

from Web2 import http_handlers, ErrorHandler
import ui_methods
import ui_modules


handler_files = os.listdir("./handlers")
for handler_f in handler_files:
    if handler_f.endswith("_handler.py"):
        __import__("Web2.handlers.%s" % handler_f[:-3])

tornado.web.ErrorHandler = ErrorHandler

handlers = []
for h in http_handlers:
    handlers.append((h.route_url, h))

ado_app = tornado.web.Application(handlers, template_path="../Web/templates", ui_modules=ui_modules,
                                  ui_methods=ui_methods)

if __name__ == "__main__":
    ado_app.listen(port=2301, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()