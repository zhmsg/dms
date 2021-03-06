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
        self._request.post(url, json=msg, as_thread=True, verify=False)
        return True

    def _send_text(self, access_token, content, at_mobiles, at_all):
        msg = dict(msgtype="text")
        msg["text"] = dict(content=content)
        if at_mobiles is not None:
            if isinstance(at_mobiles, unicode):
                at_mobiles = [at_mobiles]
            msg["at"] = dict(atMobiles=at_mobiles, isAtAll=at_all)
        return self._send(msg, access_token)

    def send_text(self, content, at_mobiles=None, at_all=False, access_token=None):
        if access_token is None:
            access_token = self.access_token
        return self._send_text(access_token, content, at_mobiles, at_all)

    def _send_link(self, access_token, content, title, message_url, pic_url):
        msg = dict(msgtype="link")
        msg["link"] = dict(text=content, messageUrl=message_url, title=title)
        if pic_url is not None:
            msg["link"]["picUrl"] = pic_url
        return self._send(msg, access_token)

    def send_link(self, content, title, message_url, pic_url=None, access_token=None):
        if access_token is None:
            access_token = self.access_token
        return self._send_link(access_token, content, title, message_url, pic_url)
