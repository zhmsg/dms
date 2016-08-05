#!/user/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from flask import request, render_template, redirect, url_for, jsonify
from flask_login import current_user


from Web import data_url_prefix, create_blue
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'

url_prefix = data_url_prefix

transport_view = create_blue('transport_view', url_prefix=url_prefix)


@transport_view.route("/records/", methods=["GET"])
def show():
    try:
        data_info = control.get_data()
        role = current_user.role
        market_role = upload_role = calc_role = False
        if role & 1 > 0:
            market_role = True
        if role & 2 > 0:
            upload_role = True
        if role & 4 > 0:
            calc_role = True
        if market_role is False and upload_role is False and calc_role is False:
            return u"您没有权限查看"
        return render_template("infoShow.html", data_info=data_info, user_name=current_user.account,
                               market_role=market_role, upload_role=upload_role, calc_role=calc_role,
                               market_target=control.market_target, market_attribute=control.market_attribute,
                               market_attribute_ch=control.market_attribute_ch, upload_attribute=control.upload_attribute,
                               upload_attribute_ch=control.upload_attribute_ch, calc_attribute=control.calc_attribute,
                               calc_attribute_ch=control.calc_attribute_ch, url_prefix=url_prefix)
    except Exception as e:
        error_message = u"获得记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/data/", methods=["POST"])
def new_data():
    try:
        result, message = control.new_data(current_user.role, current_user.account)
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/market/", methods=["POST"])
def new_market():
    try:
        request_data = request.form
        data_no = request_data["data_no"]
        market_info = {}
        for att in control.market_attribute:
            market_info[att] = request_data[att]
        result, message = control.new_market(data_no, market_info, current_user.account, current_user.role)
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/market/", methods=["GET"])
def get_market():
    try:
        data_no = int(request.args["data_no"])
        result, message = control.get_market(data_no, current_user.role)
        if result is True:
            return jsonify({"status": result, "value": message, "att": control.market_attribute, "ch": control.market_attribute_ch})
        return jsonify({"status": False, "data": message})
    except Exception as e:
        error_message = u"获得记录失败：%s" % str(e.args)
        return jsonify({"status": False, "data": error_message})


@transport_view.route("/upload/", methods=["POST"])
def new_upload():
    try:
        request_data = request.form
        data_no = request_data["data_no"]
        upload_info = {}
        for att in control.upload_attribute:
            upload_info[att] = request_data[att]
        result, message = control.new_upload(data_no, upload_info, current_user.account, current_user.role)
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/upload/", methods=["GET"])
def get_upload():
    try:
        data_no = int(request.args["data_no"])
        result, message = control.get_upload(data_no, current_user.role)
        if result is True:
            return jsonify({"status": result, "value": message, "att": control.upload_attribute, "ch": control.upload_attribute_ch})
        return jsonify({"status": False, "data": message})

    except Exception as e:
        error_message = u"获得记录失败：%s" % str(e.args)
        return jsonify({"status": False, "data": error_message})


@transport_view.route("/calc/", methods=["POST"])
def new_calc():
    try:
        request_data = request.form
        data_no = request_data["data_no"]
        calc_info = {}
        for att in control.calc_attribute:
            calc_info[att] = request_data[att]
        result, message = control.new_calc(data_no, calc_info, current_user.account, current_user.role)
        if result is False:
            return message
        return redirect(url_for("transport_view.show"))
    except Exception as e:
        error_message = u"新建记录失败：%s" % str(e.args)
        return error_message


@transport_view.route("/calc/", methods=["GET"])
def get_calc():
    try:
        data_no = int(request.args["data_no"])
        result, message = control.get_calc(data_no, current_user.role)
        if result is True:
            return jsonify({"status": result, "value": message, "att": control.calc_attribute, "ch": control.calc_attribute_ch})
        return jsonify({"status": False, "data": message})
    except Exception as e:
        error_message = u"获得记录失败：%s" % str(e.args)
        return jsonify({"status": False, "data": error_message})