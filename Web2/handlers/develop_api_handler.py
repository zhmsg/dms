#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import re
from functools import wraps
from Web2 import control, BaseAuthHandler, api_url_prefix as url_prefix, http_handlers, test_url_prefix
from Web2 import status_url_prefix


def referer_api_no(f):
    @wraps(f)
    def decorated_function(self, *args, **kwargs):
        if "Referer" not in self.request.headers:
            return self.jsonify({"status": False, "data": "Bad Request"})
        self.g.ref_url = self.request.headers["Referer"]
        find_result = re.findall("api_no=([a-z\d]{32})", self.g.ref_url)
        if len(find_result) > 0:
            self.g.api_no = find_result[0]
        elif "api_no" in self.request.args:
            self.g.api_no = self.request.args["api_no"]
        else:
            return self.jsonify({"status": False, "data": "Bad Request."})
        return f(self, *args, **kwargs)
    return decorated_function


class _BaseHandler(BaseAuthHandler):
    url_prefix = url_prefix
    route_url = url_prefix
    html_dir = "API_HELP"


class APIIndexHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/"

    def get(self):
        test_module_url = test_url_prefix + "/batch/"
        test_env_url = test_url_prefix + "/env/"
        module_url = url_prefix + "/module/"
        return self.render_template("List_API.html", test_module_url=test_module_url, module_url=module_url,
                                    test_env_url=test_env_url)


class APIInfoHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/info/"

    def get(self):
        if "api_no" not in self.request.args:
            return "Need api_no"
        api_no = self.request.args["api_no"]
        if len(api_no) != 32:
            return "Bad api_no"
        result, api_info = control.get_api_info(api_no, self.g.user_role)
        if result is False:
            return api_info
        if "X-Requested-With" in self.request.headers:
            if self.request.headers["X-Requested-With"] == "XMLHttpRequest":
                return self.jsonify({"status": True, "data": {"api_info": api_info}})
        return_url = url_prefix + "/?module_no=%s" % api_info["basic_info"]["module_no"]
        if "update" in self.request.args:
            update_stage_url = url_prefix + "/stage/"
            return self.render_template("Update_API.html", api_info=api_info, api_no=api_no, return_url=return_url,
                                        update_stage_url=update_stage_url)
        test_url = url_prefix + "/test/?api_no=%s" % api_no
        batch_test_url = url_prefix + "/test/batch/?api_no=%s" % api_no
        status_url = status_url_prefix

        return self.render_template("Show_API.html", api_info=api_info, api_no=api_no, return_url=return_url,
                                    test_url=test_url, status_url=status_url, batch_test_url=batch_test_url)


class APIModuleHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/module/"

    def get(self):
        if "module_no" not in self.request.args:
            result, part_module = control.get_part_api(self.g.user_name, self.g.user_role)
            return self.jsonify({"status": result, "data": part_module})
        module_no = int(self.request.args["module_no"])
        result, module_data = control.get_api_list(module_no, self.g.user_role)
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
        if "api_no" in self.request.args:
            api_no = self.request.args["api_no"]
            if len(api_no) != 32:
                return "Bad api_no"
            api_info_url = url_prefix + "/info/?api_no=%s" % api_no
            return self.render_template("New_API.html", part_module=part_module, api_info_url=api_info_url)
        return self.render_template("New_API.html", part_module=part_module)

    def post(self):
        request_data = self.request.json
        api_module = request_data["api_module"]

        desc = request_data["api_desc"]
        url = request_data["api_path"]
        title = request_data["api_title"]
        method = request_data["api_method"]
        module_no = int(api_module)
        if self.request.method == "PUT":
            api_no = request_data["api_no"]
            r, m = control.update_api_info(role=self.g.user_role, api_no=api_no, desc=desc, method=method, path=url,
                                           module_no=module_no, title=title)
            if r is False:
                return self.jsonify({"status": False, "data": m})
        else:
            r, api_info = control.new_api_info(module_no, title, url, method, desc, self.g.user_name, self.g.user_role)
            if r is False:
                return self.jsonify({"status": False, "data": api_info})
            api_no = api_info["api_no"]
        return self.jsonify({"status": True, "location": "%s/info/?api_no=%s" % (url_prefix, api_no), "data": "success"})

    put = post

    @referer_api_no
    def delete(self):
        result, data = control.delete_api(self.g.api_no, self.g.user_name)
        if result is False:
            return self.jsonify({"status": False, "data": data})
        return self.jsonify({"status": True, "location": url_prefix + "/", "data": "success"})


class APIStageHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/stage/"

    @referer_api_no
    def put(self):
        api_no = self.g.api_no
        stage = self.request.json["stage"]
        result, info = control.set_api_status(self.g.user_name, self.g.user_role, api_no, stage)
        if result is False:
            return self.jsonify({"status": False, "data": info})
        return self.jsonify({"status": True, "location": self.g.ref_url, "data": "success"})


class APIHeaderHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/header/"

    @referer_api_no
    def post(self):
        request_data = self.request.json
        param = request_data["name"]
        api_no = self.g.api_no
        desc = request_data["desc"]
        necessary = int(request_data["necessary"])
        result, param_info = control.add_header_param(self.g.user_name, api_no, param, necessary, desc, self.g.user_role)
        return self.jsonify({"status": result, "data": param_info})

    @referer_api_no
    def put(self):
        api_no = self.g.api_no
        request_data = self.request.json
        param = request_data["param"]
        update_type = request_data["update_type"]
        param_type = request_data["param_type"]
        if update_type == "delete":
            result, message = control.delete_predefine_param(self.g.user_role, api_no, param)
        else:
            result, message = control.add_predefine_header(self.g.user_name, api_no, param, param_type, self.g.user_role)
        return self.jsonify({"status": result, "data": message})

    @referer_api_no
    def delete(self):
        request_data = self.request.json
        api_no = self.g.api_no
        if "param" in request_data:
            result, data = control.delete_header(self.g.user_role, api_no, request_data["param"])
            return self.jsonify({"status": result, "data": data})
        return self.jsonify({"status": False, "data": "need api_no and param"})


class APIBodyHandler(_BaseHandler):
    route_url = _BaseHandler.route_url + "/body/"

    @referer_api_no
    def post(self):
        request_data = self.request.json
        param = request_data["name"]
        api_no = self.g.api_no
        desc = request_data["desc"]
        necessary = int(request_data["necessary"])
        type = request_data["type"]
        result, param_info = control.add_body_param(self.g.user_name, api_no, param, necessary, type, desc, self.g.user_role)
        return self.jsonify({"status": result, "data": param_info})

    @referer_api_no
    def put(self):
        api_no = self.g.api_no
        request_data = self.request.json
        param = request_data["param"]
        update_type = request_data["update_type"]
        param_type = "body"
        if update_type == "delete":
            result, message = control.delete_predefine_param(self.g.user_role, api_no, param)
        else:
            result, message = control.add_predefine_header(self.g.user_name, api_no, param, param_type, self.g.user_role)
        return self.jsonify({"status": result, "data": message})

    @referer_api_no
    def delete(self):
        request_data = self.request.json
        api_no = self.g.api_no
        if "api_no" in request_data and "param" in request_data:
            result, data = control.delete_body(self.g.user_role, api_no, request_data["param"])
            return self.jsonify({"status": result, "data": data})
        return self.jsonify({"status": False, "data": "need api_no and param"})

http_handlers.extend([APIIndexHandler, APIInfoHandler, APIModuleHandler, APIModuleCareHandler, APIBasicHandler])
http_handlers.extend([APIStageHandler, APIHeaderHandler, APIBodyHandler])