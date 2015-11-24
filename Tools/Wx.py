#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import datetime
import requests
import json
import tempfile
from MyEmail import MyEmailManager

my_email = MyEmailManager()


class WxManager:
    def __init__(self):
        self.token_file = ""
        self.get_token_file()

    # 基础
    def get_token_file(self):
        self.token_file = tempfile.gettempdir() + "/wx.token"

    def get_access_token(self):
        try:
            read = open(self.token_file)
            token = read.read()
            read.close()
            return token
        except Exception as e:
            error_message = str(e.args)
            my_email.send_system_exp("read wx access token ", self.token_file, error_message, 0)
            return ""

    def send_api_change_template(self, api_url, api_title, look_url, open_id, change_message):
        try:
            url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % self.get_access_token()
            request_data = {"template_id": "Jopj5DM_EDW20ovMu9h4itPYIUF7diW_12u76RndZtU"}
            request_data["touser"] = open_id
            request_data["data"] = {}
            request_data["data"]["first"] = {"value": u"非常辛苦的 %s者 您好！" % group, "color": "#173177"}
            request_data["data"]["keyword1"] = {"value": status, "color": "#173177"}
            request_data["data"]["keyword2"] = {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "color": "#000000"}
            request_data["data"]["remark"] = {"value": remark, "color": "#000000"}
            res = requests.post(url, data=json.dumps(request_data))
            if res.status_code == 200:
                r = json.loads(res.text)
                if r["errcode"] == 0:
                    return r["msgid"]
                else:
                    print(res.text)
                    return res.text
            else:
                print(res.status_code)
            return ""
        except Exception as e:
            print(e.args)
            error_message = str(e.args)
            return error_message

    def send_bug_link(self, bug_title, bug_url, open_id, title, remark):
        try:
            url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % self.get_access_token()
            request_data = {"template_id": "AlD8psjAv7E_NjUy86PnqaIgV45iuvt_ZLhxE7YJ-f0", "url": bug_url}
            request_data["touser"] = open_id
            request_data["data"] = {}
            request_data["data"]["first"] = {"value": title, "color": "#173177"}
            request_data["data"]["performance"] = {"value": bug_title, "color": "#173177"}
            request_data["data"]["time"] = {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "color": "#000000"}
            request_data["data"]["remark"] = {"value": remark, "color": "#000000"}
            res = requests.post(url, data=json.dumps(request_data))
            if res.status_code == 200:
                r = json.loads(res.text)
                if r["errcode"] == 0:
                    return r["msgid"]
                else:
                    print(res.text)
                    return res.text
            else:
                print(res.status_code)
            return ""
        except Exception as e:
            print(e.args)
            error_message = str(e.args)
            return error_message