#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Web2 import control, BaseAuthHandler, api_url_prefix as url_prefix, http_handlers

html_dir = "API_HELP"

class _BaseHandler(BaseAuthHandler):
    url_prefix = url_prefix
    route_url = url_prefix


class APIIndexHandler(_BaseHandler):
    route_url = url_prefix + "/"

    def get(self):
        result, test_env = control.get_test_env(self.g.user_role)
        if result is False:
            return test_env
        return self.render_template("%s/List_API.html" % html_dir, test_env=test_env)

    def post(self, *args, **kwargs):
        request_form = self.request.form
        api_module = request_form["api_module"]
        if api_module == "":
            return "请选择API所属模块"
        desc = request_form["api_desc"]
        url = request_form["api_url"]
        title = request_form["api_title"]
        method = request_form["api_method"]
        module_no = int(api_module)
        result, api_info = control.new_api_info(module_no, title, url, method, desc, self.g.user_name, self.g.user_role)
        if result is False:
            return api_info
        return self.redirect(url_prefix + "/update/info/?api_no=%s" % api_info["api_no"])


class APIModuleHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/module/"

    def get(self):
        if "module_no" not in self.request.args:
            return self.jsonify({"status": False, "data": "Need module_no"})
        module_no = int(self.request.args["module_no"])
        result, module_data = control.get_api_list(module_no, g.user_role)
        return self.jsonify({"status": result, "data": module_data})

    def post(self):
        request_data = self.request.json
        module_name = request_data["module_name"]
        module_prefix = request_data["module_prefix"]
        module_desc = request_data["module_desc"]
        module_part = request_data["module_part"]
        module_env = request_data["module_env"]
        if self.request.method == "POST":
            result, message = control.new_api_module(self.g.user_role, module_name, module_prefix, module_desc, module_part, module_env)
        else:
            module_no = request_data["module_no"]
            result, message = control.update_api_module(self.g.user_role, module_no, module_name, module_prefix, module_desc, module_part, module_env)
        return self.jsonify({"status": result, "data": message})

    put = post


class APIModuleCareHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/module/care/"

    def post(self, *args, **kwargs):
        request_data = self.request.json
        module_no = request_data["module_no"]
        if self.request.method == "POST":
            result, care_info = control.add_module_care(self.g.user_name, self.g.user_role, module_no)
        else:
            result, care_info = control.delete_module_care(self.g.user_name, module_no)
        return self.jsonify({"status": result, "data": care_info})

    delete = post


class APIBasicHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/basic/"

    def get(self, *args, **kwargs):
        result, part_module = control.get_part_api(self.g.user_name, self.g.user_role)
        if result is False:
            return self.write(part_module)
        module_no = 1
        if "module_no" in self.request.args:
            module_no = int(self.request.args["module_no"])
        return self.render_template("%s/New_API.html" % html_dir, part_module=part_module, url_prefix=url_prefix,
                               module_no=module_no)


http_handlers.extend([APIIndexHandler, APIModuleHandler, APIModuleCareHandler, APIBasicHandler])