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
            ["api_desc", "varchar(300)", "NO", "", None, "", "关于API的详细描述"]
        ]
        self.api_input = "api_input"
        self.api_input_desc = [
            ["input_no", "char(32)", "NO", "PRI", None, "", "主键 输入系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["input_desc", "varchar(150)", "NO", "", None, "", "API输入描述"],
            ["input_example", "text", "NO", "", None, "", "API调用输入示例"]
        ]
        self.api_output = "api_output"
        self.api_output_desc = [
            ["output_no", "char(32)", "NO", "PRI", None, "", "主键 输出系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["output_desc", "varchar(150)", "NO", "", None, "", "API输出描述"],
            ["output_example", "text", "NO", "", None, "", "API调用输出示例"]
        ]
        self.api_body = "api_body"
        self.api_body_desc = [
            ["body_no", "char(32)", "NO", "PRI", None, "", "主键 请求主体参数系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["param", "varchar(30)", "NO", "", None, "", "请求参数"],
            ["necessary", "bit(1)", "NO", "", None, "", "请求参数是否必需0非必需1必需"],
            ["type", "varchar(20)", "NO", "", None, "", "请求参数类型"],
            ["param_desc", "varchar(1000)", "NO", "", None, "", "请求参数描述"]
        ]
        self.api_header = "api_header"
        self.api_header_desc = [
            ["header_no", "char(32)", "NO", "PRI", None, "", "主键 请求头部参数系统编号"],
            ["api_no", "char(32)", "NO", "", None, "", "API系統编号 參看%s api_no" % self.api_info],
            ["param", "varchar(30)", "NO", "", None, "", "请求参数"],
            ["necessary", "bit(1)", "NO", "", None, "", "请求参数是否必需0非必需1必需"],
            ["param_desc", "varchar(1000)", "NO", "", None, "", "请求参数描述"]
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
