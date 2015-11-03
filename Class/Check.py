#! /usr/bin/env python
# coding: utf-8

import re

__author__ = 'ZhouHeng'


def check(regex, s, min_len=1, max_len=-1):
    if type(s) != unicode or type(s) !=  str:
        return False
    if min_len > 0 and len(s) < min_len:
        return False
    if max_len > 0 and len(s) > max_len:
        return False
    search_result = re.search(regex, s)
    if search_result is not None:
        return False
    return True


def check_char_num_underline(s, min_len=1, max_len=-1):
    regex = '[^a-zA-Z0-9_]'
    return check(regex, s, min_len, max_len)


def check_chinese(s, min_len=1, max_len=-1):
    regex = u'[^\u4e00-\u9fa5]'
    return check(regex, s, min_len, max_len)


def check_password(s, min_len=1, max_len=-1):
    regex = 'a-zA-Z0-9.@_'
    return check(regex, s, min_len, max_len)


def check_path(s, min_len=1, max_len=-1):
    regex = '[/a-z_]'
    return check(regex, s, min_len, max_len)

