#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB

__author__ = 'ZhouHeng'

db = DB()


class TableManager:

    def __init__(self):
        self.api_module = "api_module"
        self.api_module_desc = [
            ["module_no", "int(11)", "NO", "PRI", None, "auto_increment", "主键 自增 模块系統编号"],
            ["module_name", "varchar(35)", "NO", "", None, "", "模块的名称"],
            ["module_prefix", "varchar(35)", "NO", "", None, "", "模块的URL前綴"],
            ["module_desc", "varchar(240)", "NO", "", None, "", "关于模块的描述"]
        ]
        self.api_info = "api_info"
        self.api_info_desc = [
            ["api_no", "char(32)", "NO", "PRI", None, "", "主键 api系統编号 32位uuid"],
            ["module_no", "int(11)", "NO", "", None, "", "模块系統编号 參看%s module_no" % self.api_module],
            ["api_title", "varchar(150)", "NO", "", None, "", "API的标题即主要功能概述"],
            ["api_path", "varchar(150)", "NO", "", None, "", "API的URL"],
            ["api_method", "varchar(6)", "NO", "", None, "", "API的请求方法"],
            ["api_desc", "varchar(300)", "NO", "", None, "", "关于API的详细描述"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"]
        ]
        self.api_input = "api_input"
        self.api_input_desc = [
            ["input_no", "char(32)", "NO", "PRI", None, "", "主键 输入系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["input_desc", "varchar(550)", "NO", "", None, "", "API输入描述"],
            ["input_example", "text", "NO", "", None, "", "API调用输入示例"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"]
        ]
        self.api_output = "api_output"
        self.api_output_desc = [
            ["output_no", "char(32)", "NO", "PRI", None, "", "主键 输出系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["output_desc", "varchar(550)", "NO", "", None, "", "API输出描述"],
            ["output_example", "text", "NO", "", None, "", "API调用输出示例"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"]
        ]
        self.api_body = "api_body"
        self.api_body_desc = [
            ["body_no", "char(32)", "NO", "PRI", None, "", "主键 请求主体参数系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["param", "varchar(30)", "NO", "", None, "", "请求参数"],
            ["necessary", "bit(1)", "NO", "", None, "", "请求参数是否必需0非必需1必需"],
            ["type", "varchar(20)", "NO", "", None, "", "请求参数类型"],
            ["param_desc", "varchar(1000)", "NO", "", None, "", "请求参数描述"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"]
        ]
        self.api_header = "api_header"
        self.api_header_desc = [
            ["header_no", "char(32)", "NO", "PRI", None, "", "主键 请求头部参数系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["param", "varchar(30)", "NO", "", None, "", "请求参数"],
            ["necessary", "bit(1)", "NO", "", None, "", "请求参数是否必需0非必需1必需"],
            ["param_desc", "varchar(1000)", "NO", "", None, "", "请求参数描述"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"]
        ]
        self.api_care = "api_care"
        self.api_care_desc = [
            ["api_no", "char(32)", "NO", "PRI", None, "", "API系统编号"],
            ["user_name", "varchar(15)", "NO", "PRI", None, "", "用户账户名"],
            ["care_time", "datetime", "NO", "", None, "", "关注的时间"],
            ["level", "tinyint(4)", "NO", "", None, "", "用户关注级别 0 API的创建者 1 修改过API 2 关心API 3 删除API"]
        ]
        self.bug = "bug_info"
        self.bug_desc = [
            ["bug_no", "char(32)", "NO", "PRI", None, "", "BUG系统编号"],
            ["bug_title", "varchar(50)", "NO", "", None, "", "BUG标题"],
            ["submitter", "varchar(15)", "NO", "", None, "", "用户账户名"],
            ["submit_time", "datetime", "NO", "", None, "", "关注的时间"],
            ["bug_status", "tinyint(4)", "NO", "", 0, "", "bug 当前状态 0 代表不知BUG归属 1 代表BUG存在疑似归属者 2 代表BUG存在归属者 3 代表BUG已修复 4 代表BUG被取消 5 代表BUG属于设计范围内"]
        ]
        self.bug_owner = "bug_owner"
        self.bug_owner_desc = [
            ["bug_no", "char(32)", "NO", "PRI", None, "", "BUG系统编号"],
            ["user_name", "varchar(15)", "NO", "PRI", None, "", "用户账户名"],
            ["type", "tinyint(4)", "NO", "PRI", None, "", "1 代表疑似BUG拥有者 2 代表BUG拥有者 3 代表BUG修复者 4 代表BUG取消者 5 代表确认BUG属于设计范围内"],
            ["link_time", "datetime", "NO", "", None, "", "关联的时间"],
            ["adder", "varchar(15)", "NO", "PRI", None, "", "添加关联者账户名"]
        ]
        self.bug_example = "bug_example"
        self.bug_example_desc = [
            ["bug_no", "char(32)", "NO", "", None, "", "BUG系统编号"],
            ["type", "tinyint(4)", "NO", "", None, "", "1 文字示例 2代表 图片示例"],
            ["content", "text", "NO", "", None, "", "相应的文字示例或者时图片地址"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"]
        ]

    def create_not_exist_table(self):
        keys = vars(self).keys()
        for key in keys:
            if key.endswith("_desc") or key.endswith("_comment"):
                continue
            table_name = key
            table_desc = key + "_desc"
            if table_desc not in keys:
                print("%s need info" % table_name)
                continue
            if db.check_table(table_name, table_desc) is False:
                print("start create table %s" % table_name)
                result, message = db.create_table(eval("self.%s" % table_name), eval("self.%s" % table_desc))
                if result is True:
                    print("success create table %s" % table_name)
                else:
                    print("fail create table %s message:%s" % (table_name, message))
            else:
                print("%s table exist" % table_name)
