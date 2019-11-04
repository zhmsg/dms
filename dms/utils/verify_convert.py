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
            if i_v > max_v:
                raise BadRequest(key, "value should <=%s" % max_v)
        return i_v
    except ValueError as e:
        raise BadRequest(key, "int type required")
