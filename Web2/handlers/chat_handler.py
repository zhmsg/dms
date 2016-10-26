#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import json
import tornado.web
from Web2 import http_handlers


clients = dict()


class SocketHandler(tornado.websocket.WebSocketHandler):
    route_url = "/chat/msg/"

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

http_handlers.extend([SocketHandler])