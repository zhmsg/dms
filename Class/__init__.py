#! /usr/bin/env python
# coding: utf-8

import os

__author__ = 'ZhouHeng'

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT_STR = "%Y%m%d%H%M%S"
DATE_FORMAT_STR = "%Y%m%d"

from TableDesc import TableManager

table_manager = TableManager()

if os.path.exists("../env.conf") is False:
    env = "Development"
else:
    with open("../env.conf") as r_env:
        env = r_env.read()
