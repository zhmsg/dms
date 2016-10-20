#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Web2 import BaseHandler, http_handlers, ado_prefix, dms_url_prefix

url_prefix = ado_prefix + dms_url_prefix


class IndexHandler(BaseHandler):
    kwargs = BaseHandler.kwargs
    kwargs["url_prefix"] = url_prefix

    def get(self):
        self.kwargs["next_url"] = ""
        self.render("login.html", **IndexHandler.kwargs)


http_handlers.append((url_prefix + "/", IndexHandler))