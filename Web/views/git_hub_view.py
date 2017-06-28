#!/user/bin/env python
# -*- coding: utf-8 -*-


import sys
from flask import request, jsonify

from Web import github_url_prefix as url_prefix, create_blue
from Web import control

sys.path.append('..')

__author__ = 'Zhouheng'


git_hub_view = create_blue('git_hup_view', url_prefix=url_prefix, auth_required=False)


@git_hub_view.route("/", methods=["POST"])
def receive_github_func():
    res = request.json
    print(res)
    if res["action"] == "closed" and "pull_request" in res:
        request_num = res["number"]
        pr_info = res["pull_request"]
        request_title = pr_info["title"]
        action_user = pr_info["user"]["login"]
        request_body = pr_info["body"]
        base_branch = pr_info["base"]["ref"]
        compare_branch = pr_info["head"]["ref"]
        merged = pr_info["merged"]
        repository = res["repository"]["name"]
        info = dict(request_num=request_num, request_title=request_title, action_user=action_user,
                    request_body=request_body, base_branch=base_branch, compare_branch=compare_branch, merged=merged,
                    repository=repository)
        control.add_pull_request(**info)
    return jsonify({"status": True, "data": "success"})
