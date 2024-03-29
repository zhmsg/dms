#! /usr/bin/env python
# coding: utf-8

import sys
import time
from threading import Thread
from datetime import datetime
from Tools.Mysql_db import DB
# from JYTools import EmailManager
from .Dev import DevManager
from .APIStatus import StatusManager
from .Bug import BugManager
from .Log import LogManager
from .IP import IPManager
from .JingDuData import JingDuDataManager
from .DingMsg import DingMsgManager
from .Dyups import DyUpsManager
from .TopicMessage import MessageManager
from .WeiXin import WeiXinManager
from Class import DATE_FORMAT_STR, release_dir, jd_mysql_host, jd_mysql_db, dyups_server, wx_service, TIME_FORMAT
from Class import conf_dir

__author__ = 'ZhouHeng'

# my_email = EmailManager(conf_dir)
my_wx = WeiXinManager(wx_service)


class ControlManager(object):

    bug_status_desc = BugManager.status_desc
    bug_level_desc = BugManager.level_desc

    @staticmethod
    def judge_role(user_role, need_role):
        if user_role & need_role < need_role:
            return False
        return True

    def __init__(self):
        self.db = DB()
        self.sys_user = "sys_user"
        self.dev = DevManager()
        self.api_status = StatusManager()
        self.bug = BugManager()
        self.ip = IPManager()
        self.jd_man = JingDuDataManager(jd_mysql_host, jd_mysql_db)
        self.manger_email = ["budechao@ict.ac.cn", "biozy@ict.ac.cn"]
        self.jy_log = LogManager()
        self.ding_msg = DingMsgManager("a49a7c62e8601123cd417465ff8037cd8410a3572244903fa694e4b7548a917a")
        self.dyups_man = DyUpsManager(dyups_server)
        self.message_man = MessageManager()
        self.name_2_role_key = {"apicluster": "dyups_api", "webcluster": "dyups_web", "amscluster": "dyups_web",
                                "healthcluster": "dyups_api", "authcluster": "dyups_api", "samplecluster": "dyups_api"}

    # 针对开发者的应用
    def show_operate_auth(self, role):
        if role & self.role_value["right_new"] < self.role_value["right_new"]:
            return False, u"您没有权限"
        return self.dev.get_operate_auth()

    def list_data_table(self, role):
        if role & self.role_value["table_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.list_table()

    def get_table_info(self, table_name, role):
        if role & self.role_value["table_look"] <= 0:
            return False, u"您没有权限"
        return self.dev.get_table_info(table_name)

    def get_right_module(self, role):
        if role & self.role_value["right_look"] < self.role_value["right_look"]:
            return False, u"您没有权限"
        result, info = self.dev.get_right_module()
        return result, info

    def get_right_module_role(self, role, module_no):
        if role & self.role_value["right_look"] < self.role_value["right_look"]:
            return False, u"您没有权限"
        result, info = self.dev.get_right_module_role(module_no)
        return result, info

    def get_right_action_role(self, role, module_no):
        if role & self.role_value["right_look"] < self.role_value["right_look"]:
            return False, u"您没有权限"
        result, info = self.dev.get_right_action_role(module_no)
        return result, info

    def new_right_action(self, user_name, role, module_no, action_desc, min_role):
        if role & self.role_value["right_new"] < self.role_value["right_new"]:
            return False, u"您没有权限"
        result, info = self.dev.new_right_action(module_no, action_desc, min_role, user_name)
        return result, info

    def delete_right_action(self, user_name, role, action_no):
        if role & self.role_value["right_new"] < self.role_value["right_new"]:
            return False, u"您没有权限"
        result, info = self.dev.del_right_action(user_name, action_no)
        return result, info

    def backup_table(self, user_name, role, t_name, sql_path):
        return self.dev.backup_table(t_name, sql_path)

    def register_backup_task(self):
        return self.dev.register_backup_task()

    def get_backup_table(self):
        return self.dev.select_backup_table()

    def new_backup_table(self, user_name, user_role, t_name):
        return self.dev.insert_backup_table(t_name, user_name)

    def send_email(self, sub, data_no, info, attribute, attribute_ch):
        print("strart send email to %s" % self.manger_email)
        content = sub + "<br>"
        content += u"数据编号 : %s<br>" % data_no
        att_len = len(attribute)
        for index in range(att_len):
            content += "%s : %s<br>" % (attribute_ch[index], info[attribute[index]])
        for email in self.manger_email:
            my_email.send_mail_thread(email, sub, content)

    # 针对API状态码的应用
    def get_fun_info(self, role):
        if role & self.role_value["status_code_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_function_info()

    def get_status(self, role, *args, **kwargs):
        if role & self.role_value["status_code_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_status_code(*args, **kwargs)

    def get_error_type(self, role):
        if role & self.role_value["status_code_look"] <= 0:
            return False, u"您没有权限"
        return self.api_status.get_error_type()

    def new_service_module(self, user_name, role, service_title, service_desc):
        if role & self.role_value["status_code_module"] <= 0:
            return False, u"您没有权限"
        result, info = self.api_status.insert_service_module(service_title, service_desc)
        if result is False:
            return result, info
        service_id = info["service_id"]
        r, data = self.api_status.insert_function_module(service_id, u"公共功能模块", u"本服务模块所有功能模块可公共使用的错误状态码")
        if r is True:
            function_id = data["function_id"]
            error_info = [{"type_id": 0, "error_desc": u"访问系统正常，待用"},
                          {"type_id": 0, "error_desc": u"访问系统正常，将返回数据"},
                          {"type_id": 0, "error_desc": u"访问系统正常，仅返回成功信息"},
                          {"type_id": 0, "error_desc": u"访问系统正常，返回警告信息"},
                          {"type_id": 99, "error_desc": u"未经处理的异常，模块统一处理返回内部错误"}]
            r, data = self.api_status.new_mul_status_code(int(service_id), int(function_id), error_info, user_name)
        return result, info

    def new_function_module(self, user_name, role, service_id, function_title, function_desc):
        if role & self.role_value["status_code_module"] <= 0:
            return False, u"您没有权限"
        return self.api_status.insert_function_module(service_id, function_title, function_desc)

    def new_api_status(self, user_name, role, service_id, fun_id, type_id, error_id, error_desc):
        if role & self.role_value["status_code_new"] <= 0:
            return False, u"您没有权限"
        return self.api_status.new_status_code(service_id, fun_id, type_id, error_id, error_desc, user_name)

    def new_mul_api_status(self, user_name, role, service_id, fun_id, error_info):
        if role & self.role_value["status_code_new"] <= 0:
            return False, u"您没有权限"
        return self.api_status.new_mul_status_code(service_id, fun_id, error_info, user_name)

    def delete_api_status(self, user_name, role, status_code):
        if role & self.role_value["status_code_del"] < self.role_value["status_code_del"]:
            return False, u"您没有权限"
        return self.api_status.del_status_code(status_code)

    # 针对BUG的应用
    def get_bug_list(self, user_name, user_role):
        if self.judge_role(user_role, self.role_value["bug_look"]) is False:
            return False, u"您没有权限"
        exec_r, bug_list = self.bug.get_bug_list()
        if exec_r is True:
            bug_count = len(bug_list)
            for i in range(bug_count - 1, -1, -1):
                if bug_list[i]["bug_level"] == 0 and bug_list[i]["submitter"] != user_name:
                    bug_list.remove(bug_list[i])
        return exec_r, bug_list

    def get_my_bug_list(self, user_name, user_role):
        if self.judge_role(user_role, self.role_value["bug_look"]) is False:
            return False, u"您没有权限"
        exec_r, bug_list = self.bug.get_my_bug_list(user_name)
        return exec_r, bug_list

    def get_bug_statistic(self, role):
        if role & self.role_value["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_statistic()

    def get_bug_info(self, role, bug_no):
        if role & self.role_value["bug_look"] <= 0:
            return False, u"您没有权限"
        return self.bug.get_bug_info(bug_no)

    def get_bug_link(self, user_name, user_role, bug_no):
        if self.judge_role(user_role, self.role_value["bug_look"]) is False:
            return False, u"您没有权限"
        return self.bug.select_bug_link(bug_no)

    def new_bug(self, user_name, user_role, bug_title, bug_level):
        if self.judge_role(user_role, self.role_value["bug_new"]) is False:
            return False, u"您没有权限"
        if bug_level == 0:
            if self.judge_role(user_role, self.role_value["bug_link"]) is False:
                return False, u"您没有权限"
        return self.bug.new_bug_info(bug_title, user_name, bug_level)

    def add_bug_example(self, user_name, role, bug_no, content):
        if role & self.role_value["bug_new"] <= 0:
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
        return self.bug.new_bug_example(bug_no, content)

    def get_bug_example(self, user_name, user_role, bug_no):
        if self.judge_role(user_role, self.role_value["bug_look"]) is False:
            return False, u"您没有权限"
        return self.bug.select_bug_example(bug_no)

    def get_bug_reason(self, user_name, user_role, bug_no, submitter=None):
        if self.judge_role(user_role, self.role_value["bug_look"]) is False:
            return False, u"您没有权限"
        return self.bug.select_bug_reason(bug_no, submitter)

    def add_bug_reason(self, user_name, user_role, bug_no, bug_reason):
        if self.judge_role(user_role, self.role_value["bug_link"]) is False:
            return False, u"您没有权限"
        return self.bug.insert_bug_reason(submitter=user_name, reason=bug_reason, bug_no=bug_no)

    def update_bug_reason(self, user_name, user_role, bug_no, bug_reason):
        if self.judge_role(user_role, self.role_value["bug_link"]) is False:
            return False, u"您没有权限"
        return self.bug.update_bug_reason(submitter=user_name, reason=bug_reason, bug_no=bug_no)

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
                pass

    def _wx_send_bug_thread(self, bug_no, user_name, type, link_desc):
        t = Thread(target=self._wx_send_bug, args=(bug_no, user_name, type, link_desc))
        t.start()

    def add_bug_link(self, bug_no, user_name, role, link_user, link_type):
        if role & self.role_value["bug_new"] <= 0:
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
        exec_r, user_info = self.user.get_user_info(link_user)
        if exec_r is False:
            return False, u"添加关联账户不存在"
        link_role = user_info["role"]
        if link_role & self.role_value["bug_link"] <= 0:
            return False, u"添加关联账户无效"
        if link_type == "ys":
            if bug_status > 1:
                return False, u"BUG 状态已不允许添加疑似拥有者"
            return self._add_ys_link(bug_no, user_name, user_info)
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
        if role & self.role_value["bug_new"] <= 0:
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

    def _add_ys_link(self, bug_no, user_name, link_user_info):
        # 有new bug的权限均可添加疑似bug拥有者
        result, info = self.bug.new_bug_link(bug_no, link_user_info["user_name"], 1, user_name)
        if result is True:
            # 获得bug信息
            exec_r, bug_info = self.bug.get_bug_basic(bug_no)
            if exec_r is True:
                content = u"DMS上有人提交问题:\n" + bug_info["bug_title"]
                at_mobiles = []
                if link_user_info["tel"] is not None:
                    at_mobiles.append(link_user_info["tel"])
                self.ding_msg.send_text(content, at_mobiles)
            # 发送钉钉消息
            pass
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
            pass
        return result, info

    def _add_fix_link(self, bug_no, user_name, link_user, submitter):
        # 只有BUG提交者可以标记为修复
        if submitter != user_name:
            return False, u"您不能修改别人的BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 3, user_name)

    def _add_channel_link(self, bug_no, user_name, role, link_user, submitter):
        # 只有bug提交者才 或者拥有bug_channel 权限的人可以操作
        if submitter != user_name and role & self.role_value["bug_cancel"]:
            return False, u"您无权限修改该BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 4, user_name)

    def _add_design_link(self, bug_no, user_name, role, link_user):
        # 拥有bug_channel 权限的人可以操作
        if role & self.role_value["bug_cancel"]:
            return False, u"您无权限修改该BUG的状态"
        return self.bug.new_bug_link(bug_no, link_user, 5, user_name)

    def test_send(self, user_name, content):
        result, user_info = self.user.get_user_info(user_name)
        if result is False:
            return False, "user exception"
        if user_info["email"] is None:
            return False, "user not config email"
        my_email.send_mail_thread(user_info["email"], u"晶云文档系统测试发送与接收邮件", content)
        return True, user_info["email"]

    # 针对查看晶读平台运行日志
    def look_jy_log(self, user_name, role, start_time=None, end_time=None, level=None, search_url=None, search_account=None):
        if role & self.role_value["log_look"] <= 0:
            return False, u"您没有权限"
        result, info = self.jy_log.show_log2(start_time=start_time, end_time=end_time, level=level,
                                             search_url=search_url, search_account=search_account)
        return result, info

    def new_login_server(self, server_ip, server_name, user_ip, user_name, login_time):
        return self.jy_log.insert_login_server(server_ip, server_name, user_ip, user_name, login_time)

    def get_login_info(self):
        return self.jy_log.select_login_log()

    def query_login_info(self, limit_num=20):
        return self.jy_log.query_login_log(limit_num)

    def register_log_task(self):
        return self.jy_log.register_daily_task()

    def get_daily_log(self):
        return self.jy_log.select_daily_log()

    def get_one_log(self, user_name, role, log_no):
        if role & self.role_value["log_query"] <= 0:
            return False, "您没有权限"
        result, info = self.jy_log.select_log(log_no)
        return result, info

    def send_daily_log(self, template_html):
        result, user_list = self.user.get_role_user(self.role_value["log_receive"])
        subject = u"%s运行日志" % datetime.now().strftime(DATE_FORMAT_STR)
        if result is True:
            for u in user_list:
                my_email.send_mail(u["email"], subject, template_html)

    def register_login_task(self):
        return self.jy_log.register_login_task()

    # 查看晶读平台产生数据
    def get_project_info(self, user_name, user_role, project_no=None):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_project(project_no)

    def get_project_user(self, user_name, user_role, project_no=None, account=None):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_project_user(project_no, account)

    def get_sys_sample(self, user_name, user_role, sample_no=None):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_sample(sample_no)

    def get_sample_info(self, user_name, user_role, sample_no):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_sample_info(sample_no)

    def get_sample_user(self, user_name, user_role, sample_no=None, account=None):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_sample_user(sample_no, account)

    def query_task(self, user_name, user_role, **kwargs):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_task(**kwargs)

    def get_app_list(self, user_name, user_role):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.select_app_list()

    def query_barcode(self, user_name, user_role, **kwargs):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.query_barcode(**kwargs)

    def new_auth_code(self, user_name, user_role, **kwargs):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["jd_basic"]) is False:
            return False, "您没有权限"
        return self.jd_man.new_auth_code(**kwargs)

    # 针对工具
    def get_ip_info(self, ip_value):
        return self.ip.select_info_info(ip_value)

    # 针对发布
    def get_task(self, user_name, user_role):
        if user_role & self.role_value["release_ih_N"] <= 0:
            return False, u"您没有权限"
        return self.release_man.select_release_task()

    def new_task(self, user_name, user_role, reason, restart_service, reason_desc):
        if user_role & self.role_value["release_ih_N"] <= 0 and user_name != "system":
            return False, u"您没有权限"
        if user_role & self.role_value["release_ih_V"] <= 0 and user_name != "system" and restart_service == 0:
            return False, u"您没有权限"
        if restart_service == 0:
            result, web_pull_requests = self.release_man.select_web_pull_request()
            if len(web_pull_requests) <= 0:
                return False, u"WEB无更新不可提交"
            result, api_pull_requests = self.release_man.select_api_pull_request()
            if len(api_pull_requests) <= 0:
                return False, u"API无更新不可提交"
        elif restart_service == 1:
            result, api_pull_requests = self.release_man.select_api_pull_request()
            if len(api_pull_requests) <= 0:
                return False, u"API无更新不可提交"
        elif restart_service == 2:
            result, web_pull_requests = self.release_man.select_web_pull_request()
            if len(web_pull_requests) <= 0:
                return False, u"WEB无更新不可提交"
        result, info = self.release_man.select_release_task(user_name=user_name)
        if result is False:
            return False, info
        elif len(info) >= 2:
            return False, u"今日已不再允许预约"
        return self.release_man.new_release_task(user_name, reason, restart_service, reason_desc)

    def update_task(self, release_no, run_result):
        return self.release_man.update_release_task(release_no, run_result)

    def release_ih(self):
        return self.release_man.release_ih()

    def release_online(self, service):
        if service == "API":
            self.release_man.release_online_api()
        elif service == "WEB":
            self.release_man.release_online_web()
        return True, "success"

    # 针对pull request
    def add_pull_request(self, **kwargs):
        action_user = kwargs["action_user"]
        user_name = self.pull_request_man.select_user(action_user)
        if user_name is not None:
            exec_r, user_info = self.user.get_user_info(user_name)
            if exec_r is True:
                kwargs["user_name"] = user_info["user_name"]
                kwargs["real_name"] = user_info["nick_name"]
        return self.pull_request_man.add_pull_request(**kwargs)

    def review_pull_request(self, action_user, html_url, title, body, reviewer):
        user_name = self.pull_request_man.select_user(action_user)
        review_users = []
        for r_item in reviewer:
            user_item = self.pull_request_man.select_user(r_item)
            if user_item is not None:
                review_users.append(user_item)
        content = u"有人喊你review %s\n%s，地址是 %s" % (title, body, html_url)
        at_mobiles = []
        for u_item in review_users:
            exec_r, user_info = self.user.get_user_info(u_item)
            if exec_r is True:
                if user_info["tel"] is not None:
                    at_mobiles.append(user_info["tel"])
                content = user_info["nick_name"] + " " + content
        exec_r, user_info = self.user.get_user_info(user_name)
        if exec_r is True:
            # content = user_info["nick_name"] + content
            self.ding_msg.send_text(content, at_mobiles=at_mobiles,
                                    access_token="a49a7c62e8601123cd417465ff8037cd8410a3572244903fa694e4b7548a917a")
        return True

    # 节点管理
    def get_server_list(self, user_name, user_role, upstream_name):
        # 判断角色值
        if self.judge_role(user_role, self.role_value["dyups_look"]) is False:
            return False, "您没有权限"
        return self.dyups_man.get_server_list(upstream_name)

    def add_upstream(self, user_name, user_role, upstream_name, server_ip, server_port=80):
        if upstream_name not in self.name_2_role_key:
            return False, "无效的请求"
        role_key = self.name_2_role_key[upstream_name]
        # 判断角色值
        if self.judge_role(user_role, self.role_value[role_key]) is False:
            return False, "您没有权限"
        return self.dyups_man.add_upstream(upstream_name, server_ip, server_port)

    def remove_upstream(self, user_name, user_role, upstream_name, server_ip, server_port):
        if upstream_name not in self.name_2_role_key:
            return False, "无效的请求"
        role_key = self.name_2_role_key[upstream_name]
        # 判断角色值
        if self.judge_role(user_role, self.role_value[role_key]) is False:
            return False, "您没有权限"
        return self.dyups_man.remove_upstream(upstream_name, server_ip, server_port)

    def add_server_node(self, user_name, user_role, upstream_name, server_ip, server_port):
        if upstream_name not in self.name_2_role_key:
            return False, "无效的请求"
        role_key = self.name_2_role_key[upstream_name]
        # 判断角色值
        if self.judge_role(user_role, self.role_value[role_key]) is False:
            return False, "您没有权限"
        l = self.dyups_man.insert_server_nodes(upstream_name, server_ip, server_port, user_name)
        if l == 1:
            return True, "success"
        return False, "已存在"

    def delete_server_node(self, user_name, user_role, upstream_name, server_ip, server_port):
        if upstream_name not in self.name_2_role_key:
            return False, "无效的请求"
        role_key = self.name_2_role_key[upstream_name]
        # 判断角色值
        if self.judge_role(user_role, self.role_value[role_key]) is False:
            return False, "您没有权限"
        l = self.dyups_man.delete_server_nodes(upstream_name, server_ip, server_port, user_name)
        if l == 1:
            return True, "success"
        return False, "不存在"

    # 主题消息管理
    def new_topic_message(self, **kwargs):
        kwargs.pop("readable_content", None)
        return self.message_man.insert_topic_message(**kwargs)

    def query_topic_message(self, **kwargs):
        return self.message_man.query_message(**kwargs)

    def notification_topic_message(self, message_info, query_url=None):
        message_tag = message_info.get("message_tag", None)
        message_content = message_info["message_content"]
        if "readable_content" in message_info:
            message_content = message_info["readable_content"]
        if message_tag is None:
            _message_tag = self.message_man.default_tag
            # self.ding_msg.send_text(message_info["message_content"])
            # return 4, 60
        else:
            _message_tag = message_tag
        tags_setting = self.message_man.select_user_tag(_message_tag)
        if len(tags_setting) != 1 and _message_tag != self.message_man.default_tag:
            tags_setting = self.message_man.select_user_tag(self.message_man.default_tag)
        if len(tags_setting) != 1:
            msg_content = self.message_man.package_msg(message_tag, message_content)
            self.ding_msg.send_text(msg_content)
            return 4, 60
        tag_setting = tags_setting[0]
        notify_mode = tag_setting["notify_mode"]
        # 获取用户账户信息
        exec_r, user_info = self.user.get_user_info(tag_setting["user_name"])
        if exec_r is False:
            msg_content = self.message_man.package_msg(message_tag, message_content)
            self.ding_msg.send_text(msg_content)
            return 4, 60
        if query_url is not None:
            url = "%s?message_id=%s&topic_name=%s&topic_owner=%s" % (query_url, message_info["message_id"],
                                                                     message_info["topic_name"],
                                                                     message_info["topic_owner"])
        else:
            url = "http://dms.gene.ac"
        if self.judge_role(notify_mode, 1) is True:
            if user_info["email"] is None:
                notify_mode &= ~1
            else:
                email_content = message_content.replace("\n", "<br />")
                my_email.send_mail_thread(user_info["email"], message_tag, email_content)
        if self.judge_role(notify_mode, 2) is True:
            if user_info["wx_id"] is None:
                notify_mode &= ~2
            else:
                x = time.localtime(long(message_info["publish_time"]) / 1000)
                occur_time = time.strftime(TIME_FORMAT, x)
                mul_msg_lines = message_content.split("\n", 1)
                if len(mul_msg_lines) == 2:
                    title = mul_msg_lines[0]
                    wx_content = mul_msg_lines[1]
                else:
                    title = message_content
                    wx_content = ""
                my_wx.send_fault(message_tag, title, occur_time, wx_content, user_info["wx_id"], url)
        if self.judge_role(notify_mode, 4) is True:
            if user_info["tel"] is None or tag_setting["access_ding"] is None:
                notify_mode &= ~4
            elif tag_setting["ding_mode"] == 2:
                self.ding_msg.send_link(message_content, message_tag, url, access_token=tag_setting["access_ding"])
            else:
                msg_content = self.message_man.package_msg(message_tag, message_content)
                self.ding_msg.send_text(msg_content, access_token=tag_setting["access_ding"])
        return notify_mode, tag_setting["interval_time"]

    def new_user_topic_tag(self, user_name, user_role, message_tag, notify_mode, **kwargs):
        return self.message_man.insert_user_tag(message_tag=message_tag, user_name=user_name, notify_mode=notify_mode,
                                                **kwargs)

    def get_user_topic_tag(self, user_name, user_role):
        tags_info = self.message_man.select_user_tag()
        for item in tags_info:
            if item["user_name"] != user_name and item["access_ding"] is not None:
                item["access_ding"] = "***"
        return tags_info

    def update_user_topic_tag(self, user_name, user_role, message_tag, **kwargs):
        return self.message_man.update_user_tag(message_tag, user_name, **kwargs)

    def delete_user_topic_tag(self, user_name, user_role, message_tag):
        return self.message_man.delete_user_tag(message_tag, user_name)
