#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Tools.MyRequests import RequestsManager


class DingMsgManager(object):

    def __init__(self, access_token):
        self._request = RequestsManager()
        self.access_token = access_token
        pass

    def _send(self, msg, access_token):
        url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % access_token
        self._request.post(url, json=msg, as_thread=True)
        return True

    def _send_text(self, access_token, content, at_mobiles, at_all):
        msg = dict(msgtype="text")
        msg["text"] = dict(content=content)
        msg["at"] = dict(atMobiles=at_mobiles, isAtAll=at_all)
        return self._send(msg, access_token)

    def send_text(self, content, at_mobiles, at_all=False):
        return self._send_text(self.access_token, content, at_mobiles, at_all)