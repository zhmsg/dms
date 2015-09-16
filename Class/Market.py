#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from Check import check_chinese
from datetime import datetime

__author__ = 'ZhouHeng'


class MarketManager:

    def __init__(self):
        self.db = DB()
        self.market = "market_info"
        self.market_desc = [
            ["data_no", "int(11)", "NO", "PRI", None, ""],  # 数据编号
            ["person", "varchar(15)", "NO", "", None, ""],  # 市场负责人
            ["source", "varchar(40)", "NO", "", None, ""],  # 数据来源单位
            ["diagnosis", "varchar(40)", "NO", "", None, ""],  # 临床诊断
            ["representation", "varchar(250)", "NO", "", None, ""],  # 临床表征
            ["seq", "varchar(40)", "NO", "", None, ""],  # 测序类型
            ["num", "int(11)", "NO", "", None, ""],  # 样本数
            ["filename", "varchar(100)", "YES", "", None, ""],  # 文件名
            ["panel", "varchar(140)", "NO", "", None, ""],  # 靶向文件
            ["bedfiledir", "varchar(100)", "YES", "", None, ""],  # 靶向文件目录
            ["arrivetime", "datetime", "NO", "", None, ""],  # 数据到达时间
            ["deadline", "datetime", "NO", "", None, ""],  # 分析deadline
            ["inputtime", "datetime", "NO", "", None, ""],  # 录入时间
            ["inputuser", "varchar(15)", "NO", "", None, ""],  # 录入人
        ]
        self.attribute = ("person", "source", "diagnosis", "representation", "seq", "num",  "panel",  "arrivetime", "deadline")
        self.attribute_ch = (u"市场负责人", u"数据来源单位", u"临床诊断", u"临床表征", u"测序类型", u"样本数", u"Panel", u"数据达到时间", u"分析deadline")
        read = open("../Class/target.txt")
        target_content = read.read()
        read.close()
        self.target = target_content.split("\n")

    def create_market(self, force=False):
        return self.db.create_table(self.market, self.market_desc, force)

    def check_market(self):
        return self.db.check_table(self.market, self.market_desc)

    def new(self, data_no, market_info, inputuser):
        if check_chinese(market_info["source"], max_len=40) is False:
            return False, u"数据来源单位只能是中文且长度不大于40"
        if check_chinese(market_info["diagnosis"], max_len=40) is False:
            return False, u"临床诊断只能是中文且长度不大于40"
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = "INSERT INTO %s (data_no," % self.market
        values_sql = " VALUES ('%s'," % data_no
        for att in self.attribute:
            insert_sql += "%s," % att
            if att not in market_info:
                return False, u"upload_info缺少必要参数%s" % att
            values_sql += "'%s'," % market_info[att]
        values_sql += "'%s','%s')" % (now_time, inputuser)
        insert_sql += "inputtime,inputuser)%s" % values_sql
        self.db.execute(insert_sql)
        return True, ""
