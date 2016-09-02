#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, g
from Web import release_url_prefix as url_prefix, create_blue, user_blacklist
from Web.views import control


sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/API_HELP"


develop_release_view = create_blue('develop_release_view', url_prefix=url_prefix)


@develop_release_view.route("/", methods=["GET"])
def list_api():
    user_blacklist.append(g.user_name)
    return "true"

