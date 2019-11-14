#! /usr/bin/env python
# coding: utf-8

import re

from dms.utils.exception import BadRequest


def verify_uuid(key, s):
    if len(s) != 32:
        raise BadRequest(key, "length must be 32")
    return s

# def verify_uuid_or_enmu(key, s, enmu):
#     if s not in

def verify_int(key, i, min_v=None, max_v=None):
    try:
        i_v = int(i)
        if min_v is not None:
            if i_v < min_v:
                raise BadRequest(key, "value should >=%s" % min_v)
        if max_v is not None and i_v > max_v:
            raise BadRequest(key, "value should <=%s" % max_v)
        return i_v
    except ValueError as e:
        raise BadRequest(key, "int type required")


def verify_string(key, s, min_len=None, max_len=None):
    s_len = len(s)
    if min_len is not None and s_len < min_len:
        raise BadRequest(key, "value length should >=" % min_len)
    if max_len is not None and s_len > max_len:
        raise BadRequest(key, "value length should <=" % max_len)
    return s


URL_PATH_REG = re.compile("[^/\w<>{}:\.-]")


def verify_url_path(key, path, min_len=None, max_len=None):
    path = verify_string(key, path, min_len, max_len)
    if URL_PATH_REG.search(path):
        raise BadRequest(key, "value not allow \w<>{}-:./")
    return path

