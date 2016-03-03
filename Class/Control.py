#! /usr/bin/env python
# coding: utf-8

import sys
from threading import Thread
sys.path.append("..")
from Tools.Mysql_db import DB
from Tools.MyEmail import MyEmailManager
from Tools.Wx import WxManager
from Data import DataManager
from Market import MarketManager
from Upload import UploadManager
from Calc import CalcManager
from User import UserManager
from Dev import DevManager
from APIHelp import HelpManager
from APIStatus import StatusManager
from Bug import BugManager
from Class import table_manager

__author__ = 'ZhouHeng'

my_email = MyEmailManager()


class ControlManager:

    def __init__(self):
        self.db = DB()
        self.sys_user = "sys_user"
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
        table_manager.create_not_exist_table()
        self.api_help = HelpManager()
        self.api_status = StatusManager()
        self.bug = BugManager()
        self.manger_email = ["budechao@ict.ac.cn", "biozy@ict.ac.cn"]
        self.wx = WxManager()

    def check_user_name_exist(self, user_name, role, check_user_name):
        if role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限新建用户"
        return self.user.check_account_exist(user_name, check_user_name)

    def new_user(self, user_name, role, nick_name, creator, creator_role):
        if creator_role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限新建用户"
        if creator_role | role > creator_role:
            return False, u"给新建用户赋予权限过高"
        return self.user.new(user_name, role, nick_name, creator)

    def change_password(self, user_name, old_password, new_password):
        return self.user.change_password(user_name, old_password, new_password)

    def get_my_user(self, user_name, role):
        if role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        return self.user.my_user(user_name)

    def update_my_user_role(self, role, user_name, my_user, my_user_role):
        if role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        if role & my_user_role != my_user_role:
            return False, u"赋予权限过高"
        return self.user.update_my_user_role(my_user_role, my_user, user_name)

    def add_my_user_role(self, role, user_name, add_role, add_user_list):
        if role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        if role & add_role != add_role:
            return False, u"增加权限过高"

        return self.user.add_role_my_users(add_role, add_user_list, user_name)

    def remove_my_user_role(self, role, user_name, remove_role, remove_user_list):
        if role & self.user.role_value["user_new"] <= 0:
            return False, u"用户无权限操作用户"
        if role & remove_role != remove_role:
            return False, u"移除权限过高"
        return self.user.remove_role_my_users(remove_role, remove_user_list, user_name)

    def get_role_user(self, role):
        return self.user.get_role_user(role)

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
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_help.get_module_list()

    def new_api_module(self, role, module_name, module_prefix, module_desc):
        if role & self.user_role["api_module_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_module(module_name, module_prefix, module_desc)

    def update_api_module(self, role, module_no, module_name, module_prefix, module_desc):
        if role & self.user_role["api_module_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.update_api_module(module_no, module_name, module_prefix, module_desc)

    def delete_api_module(self, role, module_no):
        if role & self.user_role["api_module_new"] <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_module(module_no)

    def new_api_info(self, module_no, title, path, method, desc, user_name, role):
        if role & self.user_role["api_new"] <= 0:
            return False, u"您没有权限"
        result, data = self.api_help.new_api_info(module_no, title, path, method, desc)
        if result is True:
            self.api_help.new_api_care(data["api_no"], user_name, 0)
        return result, data

    def get_api_info(self, api_no, role):
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_help.get_api_info(api_no)

    def add_header_param(self, api_no, param, necessary, desc, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_api_header(api_no, {param: {"necessary": necessary, "desc": desc}})

    def add_predefine_header(self, api_no, param, role):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.new_predefine_param(api_no, param, "header")

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
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_help.get_api_list(module_no)

    def delete_header(self, role, api_no, param):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_header(api_no, param)

    def delete_predefine_param(self, role, api_no, param):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_predefine_param(api_no, param)

    def delete_body(self, role, api_no, param):
        if role & 16 <= 0:
            return False, u"您没有权限"
        return self.api_help.del_api_body(api_no=api_no, param=param)

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

    def delete_api(self, api_no, user_name):
        return self.api_help.del_api_info(api_no, user_name)

    # 针对API状态码的应用
    def get_fun_info(self, role):
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_function_info()

    def get_status(self, role):
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_status_code()

    def get_error_type(self, role):
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_error_type()

    def new_api_status(self, user_name, role, service_id, fun_id, type_id, error_id, error_desc):
        if role & self.user_role["api_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.new_status_code(service_id, fun_id, type_id, error_id, error_desc, user_name)

    # 针对BUG的应用
    def get_bug_list(self, role):
        if role & self.user_role["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_bug_list()

    def get_bug_statistic(self, role):
        if role & self.user_role["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_statistic()

    def get_bug_info(self, role, bug_no):
        if role & self.user_role["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_bug_info(bug_no)

    def new_bug(self, user_name, role, bug_title):
        if role & self.user_role["bug_new"] <= 0:
            return False, u"您没有权限"
        return self.bug.new_bug_info(bug_title, user_name)

    def add_bug_str_example(self, user_name, role, bug_no, content):
        if role & self.user_role["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断该bug是否是user_name提交的
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if submitter != user_name:
            return False, u"您不能修改别人的BUG"
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        return self.bug.new_bug_example(bug_no, 1, content)

    def add_bug_img_example(self, user_name, role, bug_no, path):
        if role & self.user_role["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断该bug是否是user_name提交的
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if submitter != user_name:
            return False, u"您不能修改别人的BUG"
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        return self.bug.new_bug_example(bug_no, 2, path)

    def _wx_send_bug(self, bug_no, user_name, type, link_desc):
        select_sql = "SELECT nick_name,wx_id,bug_title FROM %s as u,%s as b, %s as o " \
                     "WHERE u.user_name=o.user_name AND o.bug_no=b.bug_no " \
                     "AND type=%s AND u.user_name='%s' AND o.bug_no='%s';" \
                     % (self.user.user, self.bug.bug, self.bug.bug_owner, type, user_name, bug_no)
        result= self.db.execute(select_sql)
        if result != 0:
            nick_name, wx_id, bug_title = self.db.fetchone()
            if wx_id is not None:
                bug_url = "http://gene.ac/dev/bug/info?bug_no=%s" % bug_no
                title = u"%s, 您被标记为BUG %s" % (nick_name, link_desc)
                remark = u"请查看%s,如果是你的BUG，请尽快修复。" % bug_url
                self.wx.send_bug_link(bug_title, bug_url, wx_id, title, remark)

    def _wx_send_bug_thread(self, bug_no, user_name, type, link_desc):
        t = Thread(target=self._wx_send_bug, args=(bug_no, user_name, type, link_desc))
        t.start()

    def add_bug_link(self, bug_no, user_name, role, link_user, link_type):
        if role & self.user_role["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断当前bug是否允许添加关联者
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        # 判断被链接者是否可以被链接
        select_sql = "SELECT role FROM %s WHERE user_name='%s';" % (self.sys_user, link_user)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"添加关联账户不存在"
        link_role = self.db.fetchone()[0]
        if link_role & self.user_role["bug_link"] <= 0:
            return False, u"添加关联账户无效"
        if link_type == "ys":
            if bug_status > 1:
                return False, u"BUG 状态已不允许添加疑似拥有者"
            return self._add_ys_link(bug_no, user_name, link_user)
        elif link_type == "owner":
            return self._add_owner_link(bug_no, user_name, link_user, submitter)
        elif link_type == "fix":
            return self._add_fix_link(bug_no, user_name, link_user, submitter)
        elif link_type == "cancel":
            return self._add_channel_link(bug_no, user_name, role, link_user, submitter)
        elif link_type == "design":
            return self._add_design_link(bug_no, user_name, role, link_user)
        else:
            return False, u"错误的请求"

    def delete_bug_link(self, bug_no, user_name, role, link_user, link_type):
        if role & self.user_role["bug_new"] <= 0:
            return False, u"您没有权限"
        # 判断当前bug是否允许删除关联者
        select_sql = "SELECT submitter,bug_status FROM %s WHERE bug_no='%s';" % (self.bug.bug, bug_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"BUG 不存在"
        submitter, bug_status = self.db.fetchone()
        if bug_status > 2:
            return False, u"BUG 已不能修改"
        if link_type == "ys":
            if bug_status > 1:
                return False, u"BUG 状态已不允许修改疑似拥有者"
            link_type_num = 1
        elif link_type == "owner":
            link_type_num = 2
        else:
            return False, u"错误的请求"
        # 仅当当前关联者超过一个时才可以删除 其他
        select_sql = "SELECT user_name,adder FROM %s WHERE bug_no='%s' AND type=%s;" \
                     % (self.bug.bug_owner, bug_no, link_type_num)
        result = self.db.execute(select_sql)
        if result <= 1:
            return False, u"仅当关联者超过1个以后，才能删除"
        for item in self.db.fetchall():
            if item[0] == link_user and item[1] == user_name:
                return self.bug.del_bug_link(bug_no, link_user, link_type_num, user_name)
        return False, u"您无权限删除"

    def _add_ys_link(self, bug_no, user_name, link_user):
        # 有new bug的权限均可添加疑似bug拥有者
        result, info = self.bug.new_bug_link(bug_no, link_user, 1, user_name)
        if result is True:
            # 发送微信消息
            self._wx_send_bug_thread(bug_no, link_user, 1, u"疑似拥有者")
        return result, info

    def _add_owner_link(self, bug_no, user_name, link_user, submitter):
        # 判断操作者是否有权限操作 操作者可以是关联自己 或者 是bug的提交者
        if user_name != link_user:
            # 判断提交者是否是bug提交者
            if submitter != user_name:
                return False, u"您不能修改别人的BUG"
        result, info = self.bug.new_bug_link(bug_no, link_user, 2, user_name)
        if result is True:
            # 发送微信消息
            self._wx_send_bug_thread(bug_no, link_user, 2, u"拥有者")
        return result, info

    def _add_fix_link(self, bug_no, user_name, link_user, submitter):
        # 只有BUG提交者可以标记为修复
        if submitter != user_name:
            return False, u"您不能修改别人的BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 3, user_name)

    def _add_channel_link(self, bug_no, user_name, role, link_user, submitter):
        # 只有bug提交者才 或者拥有bug_channel 权限的人可以操作
        if submitter != user_name and role & self.user_role["bug_channel"]:
            return False, u"您无权限修改该BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 4, user_name)

    def _add_design_link(self, bug_no, user_name, role, link_user):
        # 拥有bug_channel 权限的人可以操作
        if role & self.user_role["bug_channel"]:
            return False, u"您无权限修改该BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 5, user_name)