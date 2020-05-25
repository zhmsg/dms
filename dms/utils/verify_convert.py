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


def verify_range_str(key, s, return_str=False):
    """
    :param s:
    :return:
    '' return None, None
    10 return  None, 10
    -10 return None, 10
    --10 return None, -10
    10- return 10, None
    -10- return -10, None
    10-100 return 10, 100
    -10-100 return -10, 100
    -100--10 return -100, -10
    """
    items = s.split('-')
    front_space = False
    l = []
    for item in items:
        if item == '':
            if front_space:
                l.append(None)
            front_space = True
        else:
            if front_space:
                value = 0 - int(item)
            else:
                value = int(item)
            l.append(value)
            front_space = False
    if front_space:
        l.append(None)
    if len(l) > 2:
        raise BadRequest(key, 'range value should at most 2 values')
    if len(l) == 1:
        l.insert(0, None)
    if l[0] is not None and l[1] is not None:
        if l[0] > l[1]:
            msg = 'left value can not greater that right value'
            raise BadRequest(key, msg)
    if return_str:
        if l[0] is None:
            return '%s' % l[1]
        ns = '-'.join(map(lambda x: '%s' % x if x is not None else '',
                          l))
        return ns
    return l


if __name__ == "__main__":
    s = {'10': [None, 10], '-10': [None, -10], '--10': [None, -10],
         '10-': [10, None], '-10-': [-10, None], '10-100': [10, 100],
         '-10-100': [-10, 100], '-100--10': [-100, -10],
         '': [None, None]}
    for _, f_v in s.items():
        r = verify_range_str('', _)
        if f_v[0] != r[0] or f_v[1] != r[1]:
            print(_)
            print(r)
