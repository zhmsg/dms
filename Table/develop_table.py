#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from TableTool import DBTool

dbt = DBTool("localhost")
dbt.create_from_dir(".")