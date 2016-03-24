#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import sys
sys.path.append("..")
from Class.TableDesc import TableManager

tm = TableManager()
tm.create_not_exist_table()