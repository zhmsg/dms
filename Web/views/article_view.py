#! /usr/bin/env python
# coding: utf-8

from flask import request, g, jsonify
from Tools.RenderTemplate import RenderTemplate
from Web import article_url_prefix as url_prefix, create_blue, control

__author__ = 'ZhouHeng'

rt = RenderTemplate("Article", url_prefix=url_prefix)
article_view = create_blue('article_view', url_prefix=url_prefix)


@article_view.route("/", methods=["GET"])
def add_func():
    article_no = ""
    if "article_no" in request.args:
        article_no = request.args["article_no"]
    if request.is_xhr is True:
        if len(article_no) != 32:
            return jsonify({"status": False, "data": "无效的编号"})
        exec_r, data = control.get_article(g.user_name, g.user_role, article_no)
        return jsonify({"status": exec_r, "data": data})
    return rt.render("add.html", article_no=article_no)


@article_view.route("/", methods=["POST"])
def add_article_action():
    request_data = request.json
    title = request_data["title"]
    abstract = request_data["abstract"]
    content = request_data["content"]
    exec_r, data = control.new_article(g.user_name, g.user_role, title, abstract, content)
    return jsonify({"status": exec_r, "data": data})


@article_view.route("/", methods=["PUT"])
def update_article_action():
    request_data = request.json
    article_no = request_data["article_no"]
    title = request_data["title"]
    abstract = request_data["abstract"]
    content = request_data["content"]
    exec_r, data = control.update_article(g.user_name, g.user_role, article_no, title, abstract, content)
    return jsonify({"status": exec_r, "data": data})


@article_view.route("/query/", methods=["GET"])
def query_func():
    if request.is_xhr is True:
        exec_r, articles = control.query_article(g.user_name, g.user_role)
        return jsonify({"status": exec_r, "data": articles})
    url_add_article = url_prefix + "/"
    return rt.render("query.html", url_add_article=url_add_article)
