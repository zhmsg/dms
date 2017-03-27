#! /usr/bin/env python
# coding: utf-8

import os
import base64
from flask import request, jsonify
from Tools.RenderTemplate import RenderTemplate
from Web import message_url_prefix as url_prefix, create_blue, verify_mns_message, redis, control

__author__ = 'ZhouHeng'

rt = RenderTemplate("message", url_prefix=url_prefix)
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
    return jsonify({"success": True, "data": "success"})
