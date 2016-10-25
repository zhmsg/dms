#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Web2 import BaseHandler, http_handlers, user_m, BaseAuthHandler
from Web2 import dms_url_prefix, dev_url_prefix, api_url_prefix, bug_url_prefix, status_url_prefix, right_url_prefix
from Web2 import log_url_prefix, param_url_prefix, release_url_prefix, control

url_prefix = dms_url_prefix


class IndexHandler(BaseHandler):
    route_url = dms_url_prefix

    def get(self):
        if self.is_authenticated:
            return self.redirect(url_prefix + "/portal/")
        self.kwargs["url_prefix"] = url_prefix
        self.kwargs["next_url"] = ""
        self.render_template("login.html")

http_handlers.append((url_prefix + "/", IndexHandler))


class LoginHandler(BaseHandler):
    route_url = dms_url_prefix + "/login/"

    def get(self):
        self.logout_user()
        self.kwargs["url_prefix"] = url_prefix
        self.kwargs["next_url"] = ""
        self.render_template("login.html")

    def post(self):
        user_name = self.get_body_argument("user_name")
        password = self.get_body_argument("password")
        result, info = user_m.check(user_name, password)
        if result is False:
            self.write(info)
        else:
            self.login_user(info["account"], info["role"])
            self.redirect(url_prefix + "/portal/")

http_handlers.append((url_prefix + "/login/", LoginHandler))


class PortalHandler(BaseAuthHandler):
    route_url = dms_url_prefix + "/portal/"

    def get(self):
        self.render_template("portal.html", api_url_prefix=api_url_prefix, dev_url_prefix=dev_url_prefix, bug_url_prefix=bug_url_prefix,
                           dms_url_prefix=dms_url_prefix, right_url_prefix=right_url_prefix,
                           log_url_prefix=log_url_prefix, param_url_prefix=param_url_prefix,
                           release_url_prefix=release_url_prefix, status_url_prefix=status_url_prefix)

http_handlers.append((url_prefix + "/portal/", PortalHandler))