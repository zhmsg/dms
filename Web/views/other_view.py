#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
from time import time
from flask import jsonify, render_template, request, g, send_from_directory
from Class.Others import OthersManager
from Tools.MyExcel import write_excel
from Web import others_url_prefix as url_prefix, create_blue, unix_timestamp

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Others"
others_man = OthersManager()

other_view = create_blue('other_view', url_prefix=url_prefix, auth_required=False)


@other_view.route("/1/", methods=["GET"])
def others_1_page():
    if "download" in request.args:
        result, info = others_man.select_others_info(1)
        if result is False:
            return info
        tmp_dir = "/tmp"
        file_name = "猝死风险预测.%s.xls" % int(time() * 1000)
        download_file = "%s/%s" % (tmp_dir, file_name)
        titles = ["患者姓名", "患者联系电话", "最大室壁厚度(mm)", "左房内径(mm)",
                  "最大（静息/Valsalva动作）左心室流出道压力阶差(mmHg)", "心源性猝死家族史", "NSVT", "不能解释晕厥",
                  "临床评估年龄（岁）", "5年心源性猝死可能性", "计算时间"]
        keys = ["extra_name", "extra_tel", "max_shibihoudu", "zuofangneijing", "yalijiecha", "cusijiazushi", "nsvt",
                "hunjue", "age", "kenengxing"]
        array_a = []
        for item in info:
            item_a = []
            result_info = json.loads(item["result_info"])
            for key in keys:
                item_a.append(result_info[key])
            item_a.append(unix_timestamp(item["insert_time"], style="datetime"))
            array_a.append(item_a)
        cols_width = [10, 15, 18, 13, 49, 16, 9, 18, 18, 19, 18]
        print write_excel(download_file, array_a=array_a, titles=titles, cols_width=cols_width)
        g.download_file = download_file
        return send_from_directory(tmp_dir, file_name, attachment_filename="猝死风险预测.xls", as_attachment=True)

    return render_template("%s/calcIndex.html" % html_dir)


@other_view.route("/1/", methods=["POST"])
def add_others_1():
    result, l = others_man.insert_others_info(1, request.json)
    return jsonify({"status": result, "data": l})
