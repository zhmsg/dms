#! /usr/bin/env python
# coding: utf-8
import sys
import requests
from flask import jsonify, request
from Tools.RenderTemplate import RenderTemplate
from Web import pay_url_prefix as url_prefix, create_blue

sys.path.append('..')

__author__ = 'Zhouheng'


rt = RenderTemplate("Pay", url_prefix=url_prefix)
pay_view = create_blue('pay_view', url_prefix=url_prefix, auth_required=False)


@pay_view.route("/real/", methods=["GET"])
@pay_view.route("/real2/", methods=["GET"])
@pay_view.route("/notreal/", methods=["GET"])
def show_param_info_func():
    return rt.render("index.html")


@pay_view.route("/real/", methods=["POST"])
@pay_view.route("/real2/", methods=["POST"])
@pay_view.route("/notreal/", methods=["POST"])
def new_billing():
    headers = dict()
    headers["X-Forwarded-For"] = dict(request.headers).get("X-Forwarded-For", "") + "," + request.remote_addr
    resp = requests.post("http://127.0.0.1:8000/api/v2/health/report/order/", auth=("zh_test", "admin0"),
                         headers=headers, json={"account": "zh_test", "billing_project": 901, "detail": "无",
                                                "remark": "1", "consumption": 1})
    print(resp.json())
    pay_info = resp.json()["data"]["pay_info"]
    pay_info["timeStamp"] = str(pay_info["timeStamp"])
    return jsonify({"status": True, "data": pay_info})