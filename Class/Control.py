#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.MyEmail import MyEmailManager
from Data import DataManager
from Market import MarketManager
from Upload import UploadManager
from Calc import CalcManager
from User import UserManager

__author__ = 'ZhouHeng'

my_email = MyEmailManager()


class ControlManager:

    def __init__(self):
        self.db = DB()
        self.data = DataManager()
        self.market = MarketManager()
        self.market_attribute = self.market.attribute
        self.market_attribute_ch = self.market.attribute_ch
        self.market_target = self.market.target
        self.upload = UploadManager()
        self.upload_attribute = self.upload.attribute
        self.upload_attribute_ch = self.upload.attribute_ch
        self.calc = CalcManager()
        self.calc_attribute = self.calc.attribute
        self.calc_attribute_ch = self.calc.attribute_ch
        self.user = UserManager()
        self.manger_email = ["budechao@ict.ac.cn"]

    def get_data(self):
        return self.data.get()

    def new_data(self, role, inputuser):
        if role != self.user.role_str[0]:
            return False, u"您的权限不足"
        result, message = self.data.new(inputuser)
        if result is True:
            if inputuser != "market":
                self.send_email(u"%s新建了一条数据记录" % inputuser, message, {}, [], [])
        return result, message

    def new_market(self, data_no, market_info, inputuser, role):
        if role != self.user.role_str[0]:
            return False, u"您的权限不足"
        data_info = self.data.get(data_no)
        if len(data_info) <= 0:
            return False, u"数据编号不存在"
        if data_info[0]["status"] != 0:
            return False, u"无修改权限"
        result, message = self.market.new(data_no, market_info, inputuser)
        if result is False:
            return False, message
        result, message = self.data.update(data_no, 1)
        if result is True:
            if inputuser != "upload":
                self.send_email(u"%s添加了市场记录" % inputuser, data_no, market_info, self.market_attribute, self.market_attribute_ch)
        return True, data_no

    def new_upload(self, data_no, upload_info, inputuser, role):
        if role != self.user.role_str[1]:
            return False, u"您的权限不足"
        data_info = self.data.get(data_no)
        if len(data_info) <= 0:
            return False, u"数据编号不存在"
        if data_info[0]["status"] != 1:
            return False, u"无修改权限"
        result, message = self.upload.new(data_no, upload_info, inputuser)
        if result is False:
            return False, message
        result, message = self.data.update(data_no, 2)
        if result is True:
            self.send_email(u"%s添加了上传记录" % inputuser, data_no, upload_info, self.upload_attribute, self.upload_attribute_ch)
        return True, ""

    def new_calc(self, data_no, calc_info, inputuser, role):
        if role != self.user.role_str[2]:
            return False, u"您的权限不足"
        data_info = self.data.get(data_no)
        if len(data_info) <= 0:
            return False, u"数据编号不存在"
        if data_info[0]["status"] != 2:
            return False, u"无修改权限"
        result, message = self.calc.new(data_no, calc_info, inputuser)
        if result is False:
            return False, message
        result, message = self.data.update(data_no, 3)
        if result is True:
            if inputuser != "calc":
                self.send_email(u"%s添加了计算记录" % inputuser, data_no, calc_info, self.calc_attribute, self.calc_attribute_ch)
        return True, ""

    def send_email(self, sub, data_no, info, attribute, attribute_ch):
        print("strart send email to %s" % self.manger_email)
        content = sub + "<br>"
        content += u"数据编号 : %s<br>" % data_no
        att_len = len(attribute)
        for index in range(att_len):
            content += "%s : %s<br>" % (attribute_ch[index], info[attribute[index]])
        for email in self.manger_email:
            my_email.send_mail_thread(email, sub, content)
