#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from urllib import parse

from flask import request, jsonify, g, redirect

from Web import short_link_prefix as url_prefix, create_blue

from dms.utils.manager import ResourcesManager

sys.path.append('..')

__author__ = 'Zhouheng'
link_man = ResourcesManager.get_instance().get_object_manager("short_link")
short_link_view = create_blue('short_link_view', url_prefix=url_prefix)


@short_link_view.route("/<int:no>/", methods=["GET"])
def get_short_link_n(no):
    exec_r, items = link_man.get_link_n_info(g.user_name, g.user_role, no)
    if exec_r is False:
        return redirect("/")
    if len(items) <= 0:
        return redirect("/")
    return redirect(items[0]["link"])


@short_link_view.route("/<s>/", methods=["GET"])
def get_short_link_s(s):
    exec_r, items = link_man.get_link_s_info(g.user_name, g.user_role, s)
    if exec_r is False:
        return redirect("/")
    if len(items) <= 0:
        return redirect("/")
    return redirect(items[0]["link"])


@short_link_view.route("/", methods=["POST"])
def create_link_func():
    r_data = request.json
    link = r_data["link"]
    url_item = parse.urlparse(link)
    if len(url_item.query) > 0:
        sorted_query = "&".join(sorted(url_item.query.split("&")))
        link = "%s://%s%s?%s" % (url_item.scheme, url_item.netloc, url_item.path, sorted_query)
    is_query = r_data.get("is_query", False)
    if is_query is True:
        exec_r, data = link_man.query_md5(link)
    else:
        s = r_data.get("s", None)
        remark = r_data["remark"]
        exec_r, data = link_man.create_link(g.user_name, g.user_role, link, remark, s)
    return jsonify({"status": exec_r, "data": data})
