#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from TableTool import DBTool

dbt = DBTool("127.0.0.1")
dbt.create_from_dir(".")
#  dbt.init_data_from_dir("Data")
