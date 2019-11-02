#! /usr/bin/env python
# coding: utf-8

import re

from dms.utils.exception import BadRequest


def verify_uuid(key, s):
    if len(s) != 32:
        raise BadRequest(key, "length must be 32")
    return s
