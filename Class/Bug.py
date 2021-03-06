#! /usr/bin/env python
# coding: utf-8

import sys
import tempfile
import uuid
from datetime import datetime, timedelta
from time import time
from Tools.Mysql_db import DB
from Class import TIME_FORMAT
from .Check import check_sql_character

temp_dir = tempfile.gettempdir()

__author__ = 'ZhouHeng'


class BugManager(object):

    level_desc = ["自己发现", "本地自己人发现", "本地开发人员发现", "测试环境自己人发现", "测试环境开发人员发现",
                  "测试环境领导发现", "测试环境其他领导发现", "生产环境自己人发现", "生产环境开发人员发现",
                  "生产环境领导发现", "生产环境其他领导发现", "生产环境客户发现", "忍无可忍"]
    status_desc = ["等待问题确认", "已有问题疑似拥有者", "已确认问题拥有者", "问题已被修复", "问题被取消", "现象正常"]

    def __init__(self):
        self.db = DB()
        self.bug = "bug_info"
        self.bug_owner = "bug_owner"
        self.bug_example = "bug_example"
        self.t_reason = "bug_reason"
        self.user = "sys_user"

    def new_bug_info(self, bug_title, submitter, bug_level):
        submit_time = datetime.now().strftime(TIME_FORMAT)
        bug_no = uuid.uuid1().hex
        if len(bug_title) < 5:
            return False, "Bad bug_title"
        bug_title = check_sql_character(bug_title)[:50]
        kwargs = {"bug_no": bug_no, "bug_title": bug_title, "submitter": submitter, "submit_time": submit_time,
                  "bug_level": bug_level}
        result = self.db.execute_insert(self.bug, kwargs=kwargs)
        if result != 1:
            return False, "sql execute result is %s " % result
        if bug_level == 0:
            self.new_bug_link(bug_no, submitter, 2, submitter)
            # self.new_bug_link(bug_no, submitter, 3, submitter)
        return True, kwargs

    def new_bug_link(self, bug_no, user_name, link_type, adder):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        link_time = datetime.now().strftime(TIME_FORMAT)
        insert_sql = "INSERT INTO %s (bug_no,user_name,type,link_time,adder) VALUES ('%s','%s','%s','%s','%s') " \
                     "ON DUPLICATE KEY UPDATE adder=adder;" \
                     % (self.bug_owner, bug_no, user_name, link_type, link_time, adder)
        result = self.db.execute(insert_sql)
        # if result != 1:
        #     return False, "sql execute result is %s " % result
        self.update_bug_status(bug_no, link_type)
        return True, {"bug_no": bug_no, "user_name": user_name, "link_type": link_type, "link_time": link_time}

    def del_bug_link(self, bug_no, user_name, link_type, adder):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        delete_sql = "DELETE FROM %s WHERE bug_no='%s' AND user_name='%s' AND adder='%s' AND type=%s;" \
                     % (self.bug_owner, bug_no, user_name, adder, link_type)
        result = self.db.execute(delete_sql)
        return True, result

    def del_bug(self, bug_no):
        if len(bug_no) != 32:
            return False, "Bad bug_no"

    def new_bug_example(self, bug_no, content):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        add_time = datetime.now().strftime(TIME_FORMAT)
        if len(content) < 5:
            return False, "Bad content"

        kwargs = {"content": content, "add_time": add_time}
        where_value = {"bug_no": bug_no}
        l = self.db.execute_update(self.bug_example, where_value=where_value, update_value=kwargs)
        kwargs.update(where_value)
        if l != 1:
            self.db.execute_insert(self.bug_example, kwargs, ignore=True)
        return True, kwargs

    def select_bug_example(self, bug_no):
        cols = ["bug_no", "content", "add_time"]
        db_items = self.db.execute_select(self.bug_example, cols=cols, where_value=dict(bug_no=bug_no))
        if len(db_items) > 0:
            return True, db_items[0]
        return True, None

    def update_bug_status(self, bug_no, status):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        update_sql = "UPDATE %s SET bug_status=%s WHERE bug_no='%s';" % (self.bug, status, bug_no)
        result = self.db.execute(update_sql)
        return True, result

    def get_bug_list(self, offset=0, num=20):
        if type(offset) != int or type(num) != int:
            return False, "Bad offset or num"
        select_sql = "SELECT bug_no,bug_title,submitter,submit_time,bug_status,bug_level FROM %s WHERE bug_status<3 " \
                     "ORDER BY bug_status,submit_time DESC LIMIT %s, %s;" % (self.bug, offset, num)
        self.db.execute(select_sql)
        bug_list = []
        for item in self.db.fetchall():
            bug_level = item[5]
            if bug_level < 0 or bug_level >= len(self.level_desc):
                continue
            bug_level_desc = self.level_desc[bug_level].decode("utf8")
            bug_list.append({"bug_no": item[0], "bug_title": item[1], "submitter": item[2],
                             "submit_time": item[3].strftime(TIME_FORMAT), "bug_status": item[4],
                             "bug_level": bug_level, "bug_level_desc": bug_level_desc})
        return True, bug_list

    def get_my_bug_list(self, user_name):
        b_cols = ["bug_no", "bug_title", "submitter", "submit_time", "bug_level", "bug_status"]
        j_cols = ["user_name", "type", "link_time"]
        where_value = dict(user_name=user_name, type=2)
        where_cond = ["bug_status<=3", "bug_status>=2"]
        bug_list = self.db.execute_select_left(self.bug, self.bug_owner, "bug_no", b_cols=b_cols, j_cols=j_cols,
                                               where_value=where_value, where_cond=where_cond, order_by=["submit_time"],
                                               order_desc=True)
        return True, bug_list

    def get_bug_basic(self, bug_no):
        where_value = dict(bug_no=bug_no)
        cols = ["bug_no", "bug_title", "submitter", "submit_time", "bug_level", "bug_status"]
        bug_list = self.db.execute_select(self.bug, where_value=where_value, cols=cols, package=True)
        if len(bug_list) <= 0:
            return False, "Not Exist"
        return True, bug_list[0]

    def get_bug_info(self, bug_no):
        if len(bug_no) != 32:
            return False, "Bad bug_no"
        # 获取基本信息
        select_sql = "SELECT bug_no,bug_title,submitter,submit_time,bug_status,bug_level,nick_name FROM %s AS i,%s AS u " \
                     "WHERE bug_no='%s' AND i.submitter=u.user_name;" \
                     % (self.bug, self.user, bug_no)
        result = self.db.execute(select_sql)
        if result != 1:
            return False, "Bad bug_no."
        info = self.db.fetchone()
        bug_level = info[5]
        if bug_level < 0 or bug_level >= len(self.level_desc):
            bug_level_desc = ""
        else:
            bug_level_desc = self.level_desc[bug_level].decode("utf8")
        basic_info = {"bug_no": info[0], "bug_title": info[1], "submitter": info[2],
                      "submit_time": info[3].strftime(TIME_FORMAT), "bug_status": info[4], "bug_level": bug_level,
                      "submit_name": info[6], "bug_level_desc": bug_level_desc}
        # 获取关联的人
        select_sql = "SELECT o.user_name,type,link_time,adder,nick_name FROM %s AS o, %s AS u " \
                     "WHERE bug_no='%s' AND o.user_name=u.user_name;" % (self.bug_owner, self.user, bug_no)
        self.db.execute(select_sql)
        link_user = {"ys": {}, "owner": {}, "fix": {}, "channel": {}, "design": {}}
        for item in self.db.fetchall():
            link_info = {"user_name": item[0], "link_type": item[1], "link_time": item[2].strftime(TIME_FORMAT),
                         "adder": item[3], "nick_name": item[4]}
            if item[1] == 1:
                link_user["ys"][item[0]] = link_info
            elif item[1] == 2:
                link_user["owner"][item[0]] = link_info
            elif item[1] == 3:
                link_user["fix"][item[0]] = link_info
            elif item[1] == 4:
                link_user["channel"][item[0]] = link_info
            elif item[1] == 5:
                link_user["design"][item[0]] = link_info
            else:
                pass
        return True, {"basic_info": basic_info, "link_user": link_user}

    def select_bug_link(self, bug_no):
        link_cols = ["user_name", "type", "link_time", "adder"]
        db_items = self.db.execute_select(self.bug_owner, where_value=dict(bug_no=bug_no), cols=link_cols)
        return True, db_items

    def get_statistic(self):
        # 获得所有的统计信息
        bug_role = 1024
        select_sql = "SELECT u.user_name,nick_name,count(bug_no) AS bug_num FROM %s as u LEFT JOIN %s as b " \
                     "on u.user_name=b.user_name AND type=2 WHERE role & %s = %s " \
                     "GROUP BY u.user_name ORDER BY bug_num DESC;" \
                     % (self.user, self.bug_owner, bug_role, bug_role)
        self.db.execute(select_sql)
        all_data = []
        for item in self.db.fetchall():
            all_data.append({"user_name": item[0], "nick_name": item[1], "bug_num": item[2]})
        # 获得最近一个月的统计信息
        after_time = (datetime.now() - timedelta(days=30)).strftime(TIME_FORMAT)
        select_sql = "SELECT u.user_name,nick_name,count(bug_no) AS bug_num FROM %s AS u LEFT JOIN %s AS b " \
                     "on u.user_name=b.user_name AND type=2 AND link_time>'%s' " \
                     "WHERE role & %s = %s GROUP BY u.user_name ORDER BY bug_num DESC;" \
                     % (self.user, self.bug_owner, after_time, bug_role, bug_role)
        self.db.execute(select_sql)
        month_data = []
        for item in self.db.fetchall():
            month_data.append({"user_name": item[0], "nick_name": item[1], "bug_num": item[2]})
        return True, {"month": month_data, "all": all_data}

    def insert_bug_reason(self, **kwargs):
        kwargs.update(dict(add_time=int(time())))
        l = self.db.execute_insert(self.t_reason, kwargs=kwargs, ignore=True)
        return True, kwargs

    def update_bug_reason(self, bug_no, submitter, reason):
        update_value = dict(reason=reason, add_time=int(time()))
        where_value = dict(bug_no=bug_no, submitter=submitter)
        l = self.db.execute_update(self.t_reason, where_value=where_value, update_value=update_value)
        update_value.update(where_value)
        return True, update_value

    def select_bug_reason(self, bug_no, submitter=None):
        where_value = dict(bug_no=bug_no)
        if submitter is not None:
            where_value["submitter"] = submitter
        reason_cols = ["bug_no", "submitter", "reason", "add_time"]
        db_items = self.db.execute_select(self.t_reason, where_value=where_value, cols=reason_cols)
        return True, db_items



