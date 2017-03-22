#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

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
        l = self.db.execute_insert(self.t_info, args=kwargs)
        return l

    def insert_content(self, article_no, content):
        kwargs = dict(article_no=article_no, content=content, insert_time=time())
        l = self.db.execute_insert(self.t_content, args=kwargs)
        return l

    def insert_statistics(self, article_no):
        kwargs = dict(article_no=article_no, update_times=1, read_times=0, self_read_times=1, comment_num=0)
        l = self.db.execute_insert(self.t_statistics, args=kwargs)
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

    def update_content(self, article_no, content):
        l = self._update_content(article_no, content)
        self._update_statistics(article_no, "update_times")
        self._update_info(article_no, update_value=dict(update_time=time()))
        return True, dict(article_no=article_no)

    def _select_content(self, article_no):
        cols = ["article_no", "content", "insert_time"]
        db_items = self.db.execute_select(self.t_content, where_value=dict(article_no=article_no), cols=cols)
        if len(db_items) < 0:
            return None
        return db_items[0]

    def _select_info(self, article_no):
        cols = ["article_no", "user_name", "title", "abstract", "update_time"]
        where_value = dict(article_no=article_no)
        db_items = self.db.execute_select(self.t_info, where_value=where_value, cols=cols)
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
