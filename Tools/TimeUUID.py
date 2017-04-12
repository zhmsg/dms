#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import uuid
from time import time


def convert_decimal(i, letters):
    s = ""
    hex_value = len(letters)
    while True:
        s = letters[i % hex_value] + s
        i /= hex_value
        if i <= 0:
            break
    return s


def to_decimal(s, letters):
    d = 0
    base = 1
    hex_value = len(letters)
    for i in range(len(s) - 1, -1, -1):
        index = letters.find(s[i])
        if index < 0:
            return False, i
        d += index * base
        base *= hex_value
    return True, d


class TimeStampUUIDException(Exception):
    def __init__(self, time_uuid, error_index, *args, **kwargs):
        super(TimeStampUUIDException, self).__init__(*args, **kwargs)
        self.time_uuid = time_uuid
        self.error_index = error_index

    def __str__(self):
        return "invalid %s. illegal %s" % (self.time_uuid, self.time_uuid[self.error_index])


class TimeStampUUID(object):
    def __init__(self, letters=None):
        self.letters = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ" if letters is None else letters

    def __call__(self, timeout=0, time_uuid=None):
        if time_uuid is None:
            time_stamp = convert_decimal(int((time() + timeout) * 1000), self.letters)
            u_id = uuid.uuid4().hex.upper()
            return time_stamp + u_id
        exec_r, time_stamp = to_decimal(time_uuid[:-32], self.letters)
        if exec_r is True:
            return time_stamp, time_uuid[-32:]
        raise TimeStampUUIDException(time_uuid, time_stamp)


class TimeStampUUID2(object):
    def __init__(self, letters=None):
        self.letters = "23456789abcdefghijklmnpqrstuvwxyz" if letters is None else letters

    def __call__(self, time_stamp=None, timeout=0, time_uuid=None):
        if time_uuid is None:
            if time_stamp is None:
                time_stamp = time()
            s_time_stamp = convert_decimal(int((time_stamp + timeout) * 1000), self.letters)
            u_id = uuid.uuid1().hex
            return s_time_stamp + u_id
        exec_r, time_stamp = to_decimal(time_uuid[:-32], self.letters)
        if exec_r is True:
            return time_stamp, time_uuid[-32:]
        raise TimeStampUUIDException(time_uuid, time_stamp)

    def min_uuid(self, time_stamp=None):
        if time_stamp is None:
            time_stamp = time()
        s_time_stamp = convert_decimal(int(time_stamp * 1000), self.letters)
        u_id = 32 * self.letters[0]
        return s_time_stamp + u_id

    def max_uuid(self, time_stamp=None):
        if time_stamp is None:
            time_stamp = time()
        s_time_stamp = convert_decimal(int(time_stamp * 1000), self.letters)
        u_id = 32 * self.letters[-1]
        return s_time_stamp + u_id
