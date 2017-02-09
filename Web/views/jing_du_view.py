#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import render_template

from Web import jingdu_url_prefix as url_prefix, create_blue

sys.path.append('..')

__author__ = 'Zhouheng'

html_dir = "/JingDu"

jing_du_view = create_blue('jing_du_view', url_prefix=url_prefix, special_protocol=True)


@jing_du_view.route("/", methods=["GET"])
def index():
    return render_template("%s/Index.html" % html_dir)
