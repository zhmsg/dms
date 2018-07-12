#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from itertools import chain
from time import time
import uuid
from Tools.Mysql_db import DB


class ArticleManager(object):
    def __init__(self):
        self.db = DB()
        self.t_info = "article_info"
        self.t_content = "article_content"
        self.t_statistics = "article_statistics"

    def insert_info(self, article_no, user_name, title, abstract):
        kwargs = dict(article_no=article_no, user_name=user_name, title=title, abstract=abstract, update_time=time())
        l = self.db.execute_insert(self.t_info, kwargs=kwargs)
        return l

    def insert_content(self, article_no, content):
        kwargs = dict(article_no=article_no, content=content, insert_time=time())
        l = self.db.execute_insert(self.t_content, kwargs=kwargs)
        return l

    def insert_statistics(self, article_no):
        kwargs = dict(article_no=article_no, update_times=1, read_times=0, self_read_times=1, comment_num=0)
        l = self.db.execute_insert(self.t_statistics, kwargs=kwargs)
        return l

    def new_article(self, user_name, title, abstract, content):
        article_no = uuid.uuid1().hex
        l = self.insert_info(article_no, user_name, title, abstract)
        l += self.insert_content(article_no, content)
        l += self.insert_statistics(article_no)
        return True, dict(article_no=article_no)

    def _update_content(self, article_no, content):
        update_value = dict(content=content)
        l = self.db.execute_update(self.t_content, where_value=dict(article_no=article_no), update_value=update_value)
        return l

    def _update_info(self, article_no, update_value):
        l = self.db.execute_update(self.t_info, where_value=dict(article_no=article_no), update_value=update_value)
        return l

    def _update_statistics(self, article_no, *args):
        update_value_list = []
        for col in args:
            update_value_list.append("%s=%s+1" % (col, col))
        l = self.db.execute_update(self.t_statistics, update_value_list=update_value_list,
                                   where_value=dict(article_no=article_no))
        return l

    def update_article(self, article_no, title=None, abstract=None, content=None):
        if content is not None:
            self._update_content(article_no, content)
        self._update_statistics(article_no, "update_times")
        update_value = dict(update_time=time())
        if title is not None:
            update_value["title"] = title
        if abstract is not None:
            update_value["abstract"] = abstract
        self._update_info(article_no, update_value=update_value)
        return True, dict(article_no=article_no)

    def _select_content(self, article_no):
        cols = ["article_no", "content", "insert_time"]
        db_items = self.db.execute_select(self.t_content, where_value=dict(article_no=article_no), cols=cols)
        if len(db_items) < 0:
            return None
        return db_items[0]

    def _select_info(self, article_no, where_cond=None, where_cond_args=None):
        cols = ["article_no", "user_name", "title", "abstract", "update_time"]
        if article_no is not None:
            where_value = dict(article_no=article_no)
        else:
            where_value = None
        db_items = self.db.execute_select(self.t_info, where_value=where_value, cols=cols, where_cond=where_cond,
                                          where_cond_args=where_cond_args)
        return db_items

    def get_article(self, article_no, user_name):
        articles = self._select_info(article_no)
        if len(articles) <= 0:
            return False, "不存在"
        article_info = articles[0]
        article_content = self._select_content(article_no)
        if article_content is None:
            return False, "文章异常"
        article_info.update(article_content)
        if article_info["user_name"] != user_name:
            self._update_statistics(article_no, "read_times")
        else:
            self._update_statistics(article_no, "self_read_times")
        return True, article_info

    def top_20_article(self):
        # 获得read_times前10篇
        # 获得self_read_times前10篇文章
        # 获得最近有人读的前10篇
        cols = ['article_no', 'read_times', 'self_read_times', 'update_times']
        items1 = self.db.execute_select(self.t_statistics, cols=cols, limit=10, order_by=["read_times"],
                                        order_desc=True)
        items2 = self.db.execute_select(self.t_statistics, cols=cols, limit=10, order_by=["self_read_times"],
                                        order_desc=True)
        items3 = self.db.execute_select(self.t_statistics, cols=cols, limit=10, order_by=["update_times"],
                                        order_desc=True)
        # 交叉合并
        items = list(chain.from_iterable(zip(items1, items2, items3)))
        if len(items) > 0:
            nos = map(lambda x: x["article_no"], items)
            where_value = dict(article_no=nos)
            cols = ["article_no", "user_name", "title", "abstract", "update_time"]
            data = self.db.execute_multi_select(self.t_info, where_value=where_value, cols=cols)
            index = 0
            i_index = 0
            while index < len(data) and i_index < len(items):
                if data[index]["article_no"] == items[i_index]["article_no"]:
                    data[index].update(items[i_index])
                    index += 1
                    i_index += 1
                else:
                    i_index += 1
            return True, data
        # 获得最新更新的文章10篇
        return True, []

    def query_article(self, **kwargs):
        if "query_str" not in kwargs:
            return self.top_20_article()
        cols = ["article_no", "user_name", "title", "abstract", "update_time"]
        sql = "SELECT {0} FROM article_info WHERE title LIKE %s OR abstract LIKE %s;".format(",".join(cols))
        arg = u"%{0}%".format(kwargs["query_str"])
        self.db.execute(sql, args=[arg, arg], auto_close=False)
        items = self.db.fetchall()
        data = []
        nos = []
        for item in items:
            d_item = dict()
            for i in range(len(cols)):
                d_item[cols[i]] = item[i]
            nos.append(d_item["article_no"])
            data.append(d_item)
        if len(data) > 0:
            cols = ['article_no', 'read_times', 'self_read_times', 'update_times']
            where_value = dict(article_no=nos)
            s_items = self.db.execute_multi_select(self.t_statistics, where_value=where_value, cols=cols)
            index = 0
            s_index = 0
            while index < len(data) and s_index < len(s_items):
                if s_items[s_index]["article_no"] == data[index]["article_no"]:
                    s_items[s_index].update(data[index])
                    index += 1
                    s_index += 1
                else:
                    index += 1
            return True, s_items
        return True, []
