#! /usr/bin/env python
# coding: utf-8

import re

__author__ = 'ZhouHeng'


def check(regex, str, min_len=1, max_len=-1):
    if min_len > 0 and len(str) < min_len:
        return False
    if max_len > 0 and len(str) > max_len:
        return False
    search_result = re.search(regex, str)
    if search_result is not None:
        return False
    return True


def check_char_num_underline(str, min_len=1, max_len=-1):
    regex = '[^a-zA-Z0-9_]'
    return check(regex, str, min_len, max_len)


def check_chinese(str, min_len=1, max_len=-1):
    regex = u'[^\u4e00-\u9fa5]'
    return check(regex, str, min_len, max_len)


def check_password(str, min_len=1, max_len=-1):
    regex = 'a-zA-Z0-9.@_'
    return check(regex, str, min_len, max_len)


