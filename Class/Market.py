#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from Tools.Mysql_db import DB
from Check import check_chinese
from datetime import datetime
from Class import TIME_FORMAT, DATE_FORMAT

__author__ = 'ZhouHeng'


class MarketManager:

    def __init__(self):
        self.db = DB()
        self.market = "market_info"
        self.attribute = ("person", "source", "diagnosis", "representation", "seq", "num",  "panel",  "arrivetime", "deadline")
        self.attribute_ch = (u"市场负责人", u"数据来源单位", u"临床诊断", u"临床表征", u"测序类型", u"样本数", u"Panel", u"数据达到时间", u"分析deadline")
        read = open("../Class/target.txt")
        target_content = read.read()
        read.close()
        self.target = target_content.split("\n")

    def new(self, data_no, market_info, inputuser):
        if check_chinese(market_info["source"], max_len=40) is False:
            return False, u"数据来源单位只能是中文且长度不大于40"
        if check_chinese(market_info["diagnosis"], max_len=40) is False:
            return False, u"临床诊断只能是中文且长度不大于40"
        now_time = datetime.now().strftime(TIME_FORMAT)
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

    def select(self, data_no):
        select_sql = "SELECT %s FROM %s WHERE data_no=%s;" % (",".join(self.attribute), self.market, data_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"数据编号不存在或没有相应记录"
        db_r = self.db.fetchone()
        market_info = {}
        len_att = len(self.attribute)
        for index in range(len_att):
            market_info[self.attribute[index]] = db_r[index]
        market_info["arrivetime"] = market_info["arrivetime"].strftime(DATE_FORMAT)
        market_info["deadline"] = market_info["deadline"].strftime(DATE_FORMAT)
        return True, market_info
