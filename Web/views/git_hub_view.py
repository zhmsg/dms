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
    elif res["action"] == "review_requested" and "pull_request" in res:
        pr_info = res["pull_request"]
        action_user = pr_info["user"]["login"]
        request_title = pr_info["title"]
        request_body = pr_info["body"]
        reviewers = pr_info["requested_reviewers"]
        r_reviewer = []
        for r_item in reviewers:
            r_reviewer.append(r_item["login"])
        html_url = pr_info["html_url"]
        control.review_pull_request(action_user, html_url, request_title, request_body, r_reviewer)
    return jsonify({"status": True, "data": "success"})
