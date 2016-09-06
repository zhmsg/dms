#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import requests


class WeiXinManager:

    def __init__(self, wx_service):
        self.wx_service = wx_service

    def send_status(self, group, open_id, env, msg):
        send_url = self.wx_service + "/template/status/"
        request_data = {"group": group, "open_id": open_id, "env": env, "msg": msg}
        response = requests.post(send_url, json=request_data, verify=False)
        res = response.json()
        if res["status"] % 10000 != 2:
            return False, res["message"]
        return True, res["message"]

    def user_info(self):
        info_url = self.wx_service + "/user/info/"
        response = requests.get(info_url, verify=False)
        res = response.json()
        if res["status"] % 10000 == 1:
            return True, res["data"]
        return False, res["message"]