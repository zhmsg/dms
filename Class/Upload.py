#! /usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
from datetime import datetime
from Tools.Mysql_db import DB
from Check import check_chinese
from Class import TIME_FORMAT, DATE_FORMAT

__author__ = 'ZhouHeng'


class UploadManager:

    def __init__(self):
        self.db = DB()
        self.upload = "upload_info"
        self.upload_desc = [
            ["data_no", "int(11)", "NO", "PRI", None, ""],  # 数据编号
            ["ossdir", "varchar(150)", "NO", "", None, ""],  # OSS上传目录
            ["person", "varchar(40)", "NO", "", None, ""],  # 上传负责人
            ["completed", "datetime", "NO", "", None, ""],  # 上传完成时间
            ["inputtime", "datetime", "NO", "", None, ""],  # 录入时间
            ["inputuser", "varchar(15)", "NO", "", None, ""],  # 录入人
        ]
        self.attribute = ("ossdir", "person", "completed")
        self.attribute_ch = (u"OSS上传目录", u"上传负责人", u"上传完成时间")

    def create_upload(self, force=False):
        return self.db.create_table(self.upload, self.upload_desc, force)

    def new(self, data_no, upload_info, inputuser):
        if check_chinese(upload_info["person"], max_len=5) is False:
            return False, u"上传负责人只能是中文且长度不大于5"
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = "INSERT INTO %s (data_no," % self.upload
        values_sql = " VALUES ('%s'," % data_no
        for att in self.attribute:
            insert_sql += "%s," % att
            if att not in upload_info:
                return False, u"upload_info缺少必要参数%s" % att
            values_sql += "'%s'," % upload_info[att]
        values_sql += "'%s','%s')" % (now_time, inputuser)
        insert_sql += "inputtime,inputuser)%s" % values_sql
        self.db.execute(insert_sql)
        return True, ""

    def select(self, data_no):
        select_sql = "SELECT %s FROM %s WHERE data_no=%s;" % (",".join(self.attribute), self.upload, data_no)
        result = self.db.execute(select_sql)
        if result == 0:
            return False, u"数据编号不存在或没有相应记录"
        db_r = self.db.fetchone()
        upload_info = {}
        len_att = len(self.attribute)
        for index in range(len_att):
            upload_info[self.attribute[index]] = db_r[index]
        upload_info["completed"] = upload_info["completed"].strftime(DATE_FORMAT)
        return True, upload_info
