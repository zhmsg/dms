#! /usr/bin/env python
# coding: utf-8

import re

__author__ = 'ZhouHeng'


def check(regex, s, min_len=1, max_len=-1):
    if type(s) != unicode and type(s) != str:
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
    regex = '[^a-zA-Z0-9_-]'
    return check(regex, s, min_len, max_len)


def check_char(s, min_len=1, max_len=-1):
    regex = '[^a-zA-Z]'
    return check(regex, s, min_len, max_len)


def check_chinese(s, min_len=1, max_len=-1):
    regex = u'[^\u4e00-\u9fa5]'
    return check(regex, s, min_len, max_len)


def check_chinese_en(s, min_len=1, max_len=-1):
    regex = u'[^\u4e00-\u9fa5a-zA-Z_]'
    return check(regex, s, min_len, max_len)


def check_password(s, min_len=1, max_len=-1):
    regex = '[^a-zA-Z0-9.@_]'
    return check(regex, s, min_len, max_len)


def check_path(s, min_len=1, max_len=-1):
    regex = r'[^/a-z_<>0-9:\.]'
    return check(regex, s, min_len, max_len)


def check_http_method(m):
    if m not in ("POST", "GET", "PUT", "DELETE"):
        return False
    return True


def check_sql_character(s):
    if type(s) != unicode and type(s) != str:
        s = str(s)
    return s.replace("\\", "\\\\").replace("'", "\\'")


def check_special_character(s):
    result = re.search("[\'\\\]", s)
    if result is not None:
        return False
    return True


def check_int(i, min_v=0, max_v=99):
    if type(i) != int:
        return False
    if i< min_v:
        return False
    if i > max_v:
        return False


def fill_zero(num, for_len):
    num_str = "%s" % num
    while for_len > 1:
        for_len -= 1
        num /= 10
        if num > 0:
            continue
        else:
            num_str = "0%s" % num_str
    return num_str


def check_account_format(account):
    if len(account) < 3 or len(account) > 20:
        return False
    m_result = re.match("[a-z]+[a-z0-9_]*", account, re.I)
    if m_result is None:
        return False
    if m_result.group() != account:
        return False
    return True

