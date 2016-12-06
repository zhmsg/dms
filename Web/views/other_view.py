#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import jsonify, render_template, request
from Class.Others import OthersManager
from Web import others_url_prefix as url_prefix, create_blue

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/Others"
others_man = OthersManager()

other_view = create_blue('other_view', url_prefix=url_prefix, auth_required=False)


@other_view.route("/1/", methods=["GET"])
def others_1_page():
    return render_template("%s/calcIndex.html" % html_dir)


@other_view.route("/1/", methods=["POST"])
def add_others_1():
    result, l = others_man.insert_others_info(1, request.json)
    return jsonify({"status": result, "data": l})
