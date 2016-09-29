#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import request, jsonify

from Web import github_url_prefix as url_prefix, create_blue
from Web.views import control

sys.path.append('..')

__author__ = 'Zhouheng'


git_hub_view = create_blue('git_hup_view', url_prefix=url_prefix, auth_required=False)


@git_hub_view.route("/", methods=["POST"])
def receive_github_func():
    res = request.json
    action_number = res["number"]
    if "pull_request" in res:
        pr_info = res["pull_request"]
        title = pr_info["title"]
        user = pr_info["user"]["login"]
        body = pr_info["body"]
        base_branch = pr_info["head"]["ref"]
        compare_branch = pr_info["base"]["ref"]
        merged = pr_info["merged"]
    repository = res["repository"]["name"]
    info = dict(action_number=action_number, title=title, user=user, body=body, base_branch=base_branch, compare_branch=compare_branch, merged=merged, repository=repository)
    print(info)
    print(request.data)
    return jsonify({"status": True, "data": "success"})