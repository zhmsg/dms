#! /usr/bin/env python
# coding: utf-8

import re
import base64
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
from Class.TopicMessage import BCMessage
from Web import message_url_prefix as url_prefix, create_blue, verify_mns_message, redis, control, login_required

__author__ = 'ZhouHeng'

rt = RenderTemplate("Message", url_prefix=url_prefix)
message_view = create_blue('message_view', url_prefix=url_prefix, auth_required=False)


@message_view.route("/receive", methods=["POST"])
def receive_message_func():
    verify_r = verify_mns_message(request.method, request.headers, request.path)
    if verify_r != 1:
        return jsonify({"success": True, "data": "not save"})
    r_data = request.json
    message_info = dict()
    coverage_keys = {"TopicOwner": "topic_owner", "PublishTime": "publish_time", "TopicName": "topic_name",
                     "SubscriptionName": "subscription_name", "MessageId": "message_id", "Message": "message_content",
                     "MessageTag": "message_tag"}
    for key in coverage_keys:
        if key in r_data:
            message_info[coverage_keys[key]] = r_data[key]
    if re.match("^[a-z\\d/\+]+=*$", message_info["message_content"], re.I) is not None:
        message_info["message_content"] = base64.b64decode(message_info["message_content"])
    if message_info["topic_name"] == "bc":
        r, h_content = BCMessage.convert_humanable(message_info["message_content"])
        if r is True:
            message_info["readable_content"] = h_content
    message_md5 = r_data["MessageMD5"]
    message_tag = message_info.get("message_tag", "")
    for key in message_info:
        if type(message_info[key]) == str:
            message_info[key] = message_info[key].decode("utf-8")
    redis_key = "message_%s_%s" % (message_tag, message_md5)
    if redis.get(redis_key) is not None:
        control.new_topic_message(**message_info)
        return jsonify({"success": True, "data": "not notification"})
    redis.setex(redis_key, "", 60)
    # 通知
    query_url = "http://" + request.host + url_prefix + "/manager/"
    notify_mode, interval_time = control.notification_topic_message(message_info, query_url)
    message_info["notify_mode"] = notify_mode
    control.new_topic_message(**message_info)
    redis.setex(redis_key, notify_mode, interval_time)
    return jsonify({"success": True, "data": "success"})


@message_view.route("/manager/", methods=["GET"])
def manager_page():
    tag_url = url_prefix + "/tag/"
    query_url = url_prefix + "/query/"
    return rt.render("Index.html", tag_url=tag_url, query_url=query_url)


@message_view.route("/tag/", methods=["GET"])
@login_required
def my_tag_data():
    tags = control.get_user_topic_tag(g.user_name, g.user_role)
    return jsonify({"status": True, "data": tags})


@message_view.route("/tag/", methods=["POST"])
@login_required
def add_tag_data():
    request_data = request.json
    message_tag = request_data["message_tag"]
    notify_mode = request_data["notify_mode"]
    access_ding = request_data.get("access_ding", None)
    ding_mode = int(request_data.get("ding_mode", "1"))
    interval_time = request_data["interval_time"]
    l = control.new_user_topic_tag(g.user_name, g.user_role, message_tag, notify_mode, access_ding=access_ding,
                                   ding_mode=ding_mode, interval_time=interval_time)
    if l == 1:
        return jsonify({"status": True, "data": message_tag, "location": url_prefix + "/manager/"})
    else:
        return jsonify({"status": False, "data": "标签可能已存在"})


@message_view.route("/tag/", methods=["PUT"])
@login_required
def update_tag_data():
    request_data = request.json
    allow_keys = ["message_tag", "notify_mode", "access_ding", "ding_mode", "interval_time"]
    for key in request_data:
        if key not in allow_keys:
            return jsonify({"status": False, "data": "Not Allow %s" % key})
    l = control.update_user_topic_tag(g.user_name, g.user_role, **request_data)
    request_data["exec_r"] = l
    request_data["op"] = "PUT"
    return jsonify({"status": True, "data": request_data})


@message_view.route("/tag/", methods=["DELETE"])
@login_required
def delete_tag_data():
    request_data = request.json
    message_tag = request_data["message_tag"]
    l = control.delete_user_topic_tag(g.user_name, g.user_role, message_tag)
    request_data["exec_r"] = l
    request_data["op"] = "DELETE"
    return jsonify({"status": True, "data": request_data})


@message_view.route("/query/", methods=["GET"])
def query_message():
    message_id = request.args["message_id"]
    topic_owner = "1530531001163833"
    if "topic_owner" in request.args:
        topic_owner = request.args["topic_owner"]
    topic_name = "JYWaring"
    if "topic_name" in request.args:
        topic_name = request.args["topic_name"]
    db_items = control.query_topic_message(topic_owner=topic_owner, topic_name=topic_name, message_id=message_id)
    return jsonify({"status": True, "data": db_items})
