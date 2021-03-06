#! /usr/bin/env python
# coding: utf-8

import json
from time import time
from Tools.Mysql_db import DB

__author__ = 'ZhouHeng'


class MessageManager(object):

    default_tag = "DMS"

    def __init__(self):
        self.db = DB()
        self.t_msg = "topic_message_content"
        self.t_user_tag = "user_topic_tag"

    @staticmethod
    def package_msg(message_tag, message_content):
        s = ""
        if message_tag:
            s += u"#%s#\n" % message_tag
        s += message_content
        return s

    def insert_topic_message(self, **kwargs):
        kwargs["insert_time"] = int(time())
        l = self.db.execute_insert(self.t_msg, kwargs=kwargs, ignore=True)
        return l

    def insert_user_tag(self, **kwargs):
        kwargs["update_time"] = kwargs["insert_time"] = time()
        l = self.db.execute_insert(self.t_user_tag, kwargs=kwargs, ignore=True)
        return l

    def update_user_tag(self, message_tag, user_name, **kwargs):
        where_value = dict(message_tag=message_tag, user_name=user_name)
        kwargs["update_time"] = time()
        l = self.db.execute_update(self.t_user_tag, update_value=kwargs, where_value=where_value)
        return l

    def select_user_tag(self, message_tag=None):
        if message_tag is not None:
            where_value = dict(message_tag=message_tag)
        else:
            where_value = None
        cols = ["message_tag", "user_name", "notify_mode", "access_ding", "ding_mode", "interval_time", "insert_time",
                "update_time"]
        db_items = self.db.execute_select(self.t_user_tag, where_value=where_value, cols=cols)
        return db_items

    def delete_user_tag(self, message_tag, user_name):
        where_value = dict(message_tag=message_tag, user_name=user_name)
        l = self.db.execute_delete(self.t_user_tag, where_value=where_value)
        return l

    def query_message(self, **kwargs):
        cols = ["topic_owner", "topic_name", "message_id", "subscription_name", "message_tag", "notify_mode",
                "publish_time", "insert_time", "message_content"]
        db_items = self.db.execute_select(self.t_msg, where_value=kwargs, cols=cols)
        return db_items


class BCMessage(object):

    category = dict(Job=u"DAG作业")
    event = dict(OnJobFinished=u"作业已经结束", OnJobWaiting=u"作业开始等待", OnJobStopped=u"作业被终止",
                 OnJobFailded=u"作业挂掉了", OnJobRunning=u"作业开始运行")
    state = dict(Finished=u"结束了", Stopped="被停止了")

    cn_desc = [
        ["JobId", u"作业ID"],
        ["InstanceId", u"实例ID"]
    ]

    @staticmethod
    def convert_humanable(msg):
        try:
            o = json.loads(msg)
        except ValueError:
            return False, None
        h_msg = ""
        if "Category" in o:
            if o["Category"] in BCMessage.category:
                c = BCMessage.category[o["Category"]]
            else:
                c = o["Category"]
            h_msg += u"作业类型: %s\n" % c
        if "JobName" in o:
            h_msg += u"作业名称: %s\n" % o["JobName"]
        if "Task" in o:
            h_msg += u"任务名称: %s\n" % o["Task"]
        if "Event" in o:
            e = o["Event"]
            if e in BCMessage.event:
                e = BCMessage.event[e]
            h_msg += u"推送事件: %s\n" % e
        if "State" in o:
            s = o["State"]
            if s in BCMessage.state:
                s = BCMessage.state[s]
            h_msg += u"状态: %s\n" % s
        for item in BCMessage.cn_desc:
            if item[0] in o:
                h_msg += u"%s: %s\n" % (item[1], o[item[0]])
        return True, h_msg
