#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import request, jsonify, g, redirect

from Web import short_link_prefix as url_prefix, create_blue
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'

short_link_view = create_blue('short_link_view', url_prefix=url_prefix)


@short_link_view.route("/<int:no>/", methods=["GET"])
def get_short_link_n(no):
    exec_r, items = control.get_link_n_info(g.user_name, g.user_role, no)
    if exec_r is False:
        return redirect("/")
    if len(items) <= 0:
        return redirect("/")
    return redirect(items[0]["link"])


@short_link_view.route("/<s>/", methods=["GET"])
def get_short_link_s(s):
    exec_r, items = control.get_link_s_info(g.user_name, g.user_role, s)
    if exec_r is False:
        return redirect("/")
    if len(items) <= 0:
        return redirect("/")
    return redirect(items[0]["link"])
