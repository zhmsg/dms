#! /usr/bin/env python
# coding: utf-8

import os
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
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"],
            ["update_time", "datetime", "NO", "", None, "", "最近更新的时间"]
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

        self.service_module = "service_module"
        self.service_module_desc = [
            ["service_id", "int(11)", "NO", "PRI", None, "", "服务模块系统编号 主键"],
            ["service_title", "varchar(40)", "NO", "", None, "", "服务模块标题"],
            ["service_desc", "varchar(500)", "NO", "", None, "", "服务模块描述"]
        ]
        self.service_module_comment = "服务模块相关信息"
        self.service_module_init = True
        self.function_module = "function_module"
        self.function_module_desc = [
            ["service_id", "tinyint(11)", "NO", "PRI", None, "", "服务模块系统编号 联合主键"],
            ["function_id", "tinyint(11)", "NO", "PRI", None, "", "功能模块编号 联合主键"],
            ["function_title", "varchar(100)", "NO", "", None, "", "功能模块标题"],
            ["function_desc", "varchar(500)", "NO", "", None, "", "功能模块描述"]
        ]
        self.function_module_comment = "功能模块相关信息"
        self.function_module_init = True
        self.error_type = "error_type"
        self.error_type_desc = [
            ["type_id", "tinyint(11)", "NO", "PRI", None, "", "错误类型编号主键"],
            ["type_title", "varchar(100)", "NO", "", None, "", "功能模块标题"],
            ["type_desc", "varchar(500)", "NO", "", None, "", "功能模块描述"]
        ]
        self.error_type_comment = "错误类型相关信息"
        self.error_type_init = True
        self.status_code = "status_code"
        self.status_code_desc = [
            ["status_code", "int(4)", "NO", "PRI", None, "", "状态码 主键"],
            ["code_desc", "varchar(500)", "NO", "", None, "", "状态码描述"],
            ["add_time", "datetime", "NO", "", None, "", "添加的时间"],
            ["adder", "varchar(15)", "NO", "", None, "", "添加者账户名"]
        ]
        self.status_code_comment = "错误状态码相关信息"

    def create_not_exist_table(self):
        keys = vars(self).keys()
        for key in keys:
            if key.endswith("_desc") or key.endswith("_comment") or key.endswith("_init"):
                continue
            table_name = eval("self.%s" % key)
            table_desc = key + "_desc"
            table_init = key + "_init"
            if table_desc not in keys:
                print("%s need info" % table_name)
                continue
            if db.check_table(table_name, table_desc) is False:
                print("start create table %s" % table_name)
                result, message = db.create_table(table_name, eval("self.%s" % table_desc))
                if result is True:
                    print("success create table %s" % table_name)
                else:
                    print("fail create table %s message:%s" % (table_name, message))
            else:
                print("%s table exist" % table_name)
            if table_init in keys and eval("self.%s" % table_init) is True:
                result, message = self.init_table(table_name)
                if result is True:
                    print("success init table %s" % table_name)
                else:
                    print("fail init table %s message:%s" % (table_name, message))

    def init_table(self, table_name):
        keys = vars(self).keys()
        if table_name not in keys or table_name + "_desc" not in keys:
            return False, "bad table_name"
        table_desc = eval("self.%s_desc" % table_name)
        len_col = len(table_desc)
        file_path = "../Data/%s.data" % table_name
        if os.path.exists(file_path) is False:
            return False, "file not exist"
        read = open(file_path)
        content = read.read()
        read.close()
        lines = content.split("\n")
        insert_sql_for = "INSERT IGNORE INTO %s VALUES {0} " % table_name
        value_sql = ""
        for line in lines:
            if len(value_sql) >= 10000:
                insert_sql = insert_sql_for.format(value_sql[:-1])
                db.execute(insert_sql[:-1])
                value_sql = ""
            if len(line) <= 0:
                continue
            data = line.split("\t")
            if len(data) != len_col:
                print(data)
                return False, "Bad data file"
            value_sql += "("
            for v in data:
                value_sql += "'%s'," % v
            value_sql = value_sql[:-1] + "),"
        if value_sql != "":
            insert_sql = insert_sql_for.format(value_sql[:-1])
            db.execute(insert_sql[:-1])
        return True, "success"

