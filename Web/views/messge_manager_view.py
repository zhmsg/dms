#! /usr/bin/env python
# coding: utf-8

import base64
from flask import request, jsonify, g
from Tools.RenderTemplate import RenderTemplate
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
    message_info["message_content"] = base64.b64decode(message_info["message_content"])
    message_md5 = r_data["MessageMD5"]
    message_tag = message_info.get("message_tag", "")
    redis_key = "message_%s_%s" % (message_tag, message_md5)
    if redis.get(redis_key) is not None:
        control.new_topic_message(**message_info)
        return jsonify({"success": True, "data": "not notification"})
    redis.setex(redis_key, "", 60)
    # 通知
    notify_mode, interval_time = control.notification_topic_message(message_info)
    message_info["notify_mode"] = notify_mode
    control.new_topic_message(**message_info)
    redis.setex(redis_key, notify_mode, interval_time)
    return jsonify({"success": True, "data": "success"})


@message_view.route("/manager/", methods=["GET"])
@login_required
def manager_page():
    tag_url = url_prefix + "/tag/"
    return rt.render("Index.html", tag_url=tag_url)


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
    interval_time = request_data["interval_time"]
    l = control.new_user_topic_tag(g.user_name, g.user_role, message_tag, notify_mode, access_ding, interval_time)
    if l == 1:
        return jsonify({"status": True, "data": message_tag, "location": url_prefix + "/manager/"})
    else:
        return jsonify({"status": False, "data": "标签可能已存在"})


@message_view.route("/tag/", methods=["PUT"])
@login_required
def update_tag_data():
    request_data = request.json
    allow_keys = ["message_tag", "notify_mode", "access_ding", "interval_time"]
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
