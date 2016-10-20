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

from Web2 import http_handlers
import ui_methods
import ui_modules


clients = dict()


class SocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    @staticmethod
    def send_to_all(message):
        for key in clients.keys():
            clients[key]["c"].write_message(message)

    def open(self):
        self.write_message({"msg_type": "sys", "msg": 'Connect Success', "sender": "system"})

    def on_message(self, message):
        msg_info = json.loads(message)
        if msg_info["msg_type"] == "login":
            clients[str(id(self))] = {"c": self, "user_name": msg_info["data"]}
            self.write_message({"msg_type": "sys", "msg": msg_info["data"] + ' Login Success', "sender": "system"})
        elif str(id(self)) in clients:
            send_msg = {"msg_type": "msg", "msg": msg_info["data"], "sender": clients[str(id(self))]["user_name"]}
            SocketHandler.send_to_all(send_msg)
        else:
            return

    def on_close(self):
        del clients[str(id(self))]

http_handlers.append(('/chat/msg/', SocketHandler))
handler_files = os.listdir("./handlers")
for handler_f in handler_files:
    if handler_f.endswith("_handler.py"):
        __import__("Web2.handlers.%s" % handler_f[:-3])


if __name__ == "__main__":
    ado_app = tornado.web.Application(http_handlers, template_path="templates", ui_modules=ui_modules, ui_methods=ui_methods, debug=True)
    ado_app.listen(port=2300, address="127.0.0.1")
    tornado.ioloop.IOLoop.instance().start()