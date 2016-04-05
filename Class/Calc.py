#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from Check import check_chinese
from datetime import datetime
from Class import TIME_FORMAT, DATE_FORMAT

__author__ = 'ZhouHeng'


class CalcManager:

    def __init__(self):
        self.db = DB()
        self.calc = "calc_info"
        self.attribute = ("completed", "import", "account", "project_no", "person")
        self.attribute_ch = (u"计算完成时间", u"导入平台时间", u"导入账户", u"导入项目号", u"计算负责人")

    def new(self, data_no, calc_info, inputuser):
        if check_chinese(calc_info["person"], max_len=5) is False:
            return False, u"计算负责人只能是中文且长度不大于5"
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = "INSERT INTO %s (data_no," % self.calc
        values_sql = " VALUES ('%s'," % data_no
        for att in self.attribute:
            insert_sql += "%s," % att
            if att not in calc_info:
                return False, u"calc_info缺少必要参数%s" % att
            values_sql += "'%s'," % calc_info[att]
        values_sql += "'%s','%s')" % (now_time, inputuser)
        insert_sql += "inputtime,inputuser)%s" % values_sql
        self.db.execute(insert_sql)
        return True, ""

    def select(self, data_no):
        select_sql = "SELECT %s FROM %s WHERE data_no=%s;" % (",".join(self.attribute), self.calc, data_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"数据编号不存在或没有相应记录"
        db_r = self.db.fetchone()
        calc_info = {}
        len_att = len(self.attribute)
        for index in range(len_att):
            calc_info[self.attribute[index]] = db_r[index]
        calc_info["completed"] = calc_info["completed"].strftime(DATE_FORMAT)
        return True, calc_info
