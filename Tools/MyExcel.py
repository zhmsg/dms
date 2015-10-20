#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import xlwt
import os


def write_excel(save_path, array_a, titles=[]):
    try:
        (dir, file_name) = os.path.split(save_path)
        file = xlwt.Workbook()
        table = file.add_sheet(file_name.strip(".xls"), cell_overwrite_ok=True)
        offset = 0
        if (type(titles) == list or type(titles) == tuple) and len(titles) > 0:
            for index in range(len(titles)):
                table.write(0, index, titles[index])
            offset = 1
        for index in range(len(array_a)):
            arr = array_a[index]
            for i in range(len(arr)):
                value = arr[i]
                table.write(index + offset, i, value)
        file.save(save_path)
        return True, save_path
    except Exception as e:
        error_message = "write excel error:%s" % str(e.args)
        return False, error_message
"""
# Example
titles = ["title1", "title2", "title3", "title4"]
array_a = [["value11", "value12", "value13", "value14"],
           ["value21", "value22", "value23", "value24"]]
result, message = write_excel("/home/msg/save_path.xls", array_a, titles)
if result is True:
    print("Save Success, Path is %s" % message)
else:
    print("Save Fail, Error is %s" % message)
"""