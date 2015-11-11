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
from Dev import DevManager
from APIHelp import HelpManager
from Class import table_manager

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
        self.user_role = self.user.role_value
        self.dev = DevManager()
        # table_manager.create_not_exist_table()
        self.api_help = HelpManager()
        self.manger_email = ["budechao@ict.ac.cn", "biozy@ict.ac.cn"]

    def new_user(self, user_name, password, role, nick_name, creator, creator_role):
        if creator_role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限新建用户"
        if creator_role | role > creator_role:
            return False, u"给新建用户赋予权限过高"
        return self.user.new(user_name, password, role, nick_name, creator)

    def get_data(self):
        return self.data.get()

    def new_data(self, role, inputuser):
        if (role & 1) <= 0:
            return False, u"您的权限不足"
        result, message = self.data.new(inputuser)
        return result, message

    def new_market(self, data_no, market_info, inputuser, role):
        if (role & 1) <= 0:
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
        if (role & 2) <= 0:
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
        if (role & 4) <= 0:
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

    def get_market(self, data_no, role):
        if (role & 1) <= 0:
            return False, u"您的权限不足"
        return self.market.select(data_no)

    def get_upload(self, data_no, role):
        if (role & 2) <= 0:
            return False, u"您的权限不足"
        return self.upload.select(data_no)

    def get_calc(self, data_no, role):
        if (role & 4) <= 0:
            return False, u"您的权限不足"
        return self.calc.select(data_no)

    # 针对开发者的应用
    def download_operate_auth(self, role):
        if role & self.user_role["auth_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.get_operate_auth_file()

    def show_operate_auth(self, role):
        if role & self.user_role["auth_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.get_operate_auth()

    def list_data_table(self, role):
        if role & self.user_role["table_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.list_table()

    def get_table_info(self, table_name, role):
        if role & self.user_role["table_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.get_table_info(table_name)

    def send_email(self, sub, data_no, info, attribute, attribute_ch):
        print("strart send email to %s" % self.manger_email)
        content = sub + "<br>"
        content += u"数据编号 : %s<br>" % data_no
        att_len = len(attribute)
        for index in range(att_len):
            content += "%s : %s<br>" % (attribute_ch[index], info[attribute[index]])
        for email in self.manger_email:
            my_email.send_mail_thread(email, sub, content)

    # 针对API HELP的应用
    def get_module_list(self, role):
        if role & 8 <= 0:
            return False, u"您没有权限"
        return self.api_help.get_module_list()

    def new_api_info(self, module_no, title, path, method, desc, user_name, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        result, data = self.api_help.new_api_info(module_no, title, path, method, desc)
        if result is True:
            self.api_help.new_api_care(data["api_no"], user_name, 0)
        return result, data

    def get_api_info(self, api_no, role):
        if role & 8 <= 0:
            return False, u"您没有权限"
        return self.api_help.get_api_info(api_no)

    def add_header_param(self, api_no, param, necessary, desc, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_header(api_no, {param :{"necessary": necessary, "desc": desc}})

    def add_body_param(self, api_no, param, necessary, type, desc, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_body(api_no, {param :{"necessary": necessary, "type": type, "desc": desc}})

    def add_input_example(self, api_no, example, desc, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_input(api_no, [{"desc": desc, "example": example}])

    def add_output_example(self, api_no, example, desc, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_output(api_no, [{"desc": desc, "example": example}])

    def add_care(self, api_no, user_name, role):
        if role & 8 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_care(api_no, user_name)

    def get_api_list(self, module_no, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.get_api_list(module_no)

    def delete_header(self, header_no, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_header(header_no)

    def delete_body(self, body_no, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_body(body_no)

    def delete_input(self, input_no, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_input(input_no)

    def delete_ouput(self, output_no, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_output(output_no)

    def delete_care(self, api_no, user_name):
        return self.api_help.del_api_care(api_no, user_name)