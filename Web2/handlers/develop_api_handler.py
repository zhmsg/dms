#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Web2 import control, BaseAuthHandler, test_url_prefix, api_url_prefix as url_prefix, http_handlers

html_dir = "API_HELP"

class _BaseHandler(BaseAuthHandler):
    url_prefix = url_prefix
    route_url = url_prefix


class APIIndexHandler(_BaseHandler):
    route_url = url_prefix + "/"

    def get(self):
        result, part_module = control.get_part_api(self.g.user_name, self.g.user_role)
        if result is False:
            return part_module
        if self.g.user_role & control.role_value["api_module_new"] == control.role_value["api_module_new"]:
            new_power = True
        else:
            new_power = False
        result, test_env = control.get_test_env(self.g.user_role)
        if result is False:
            return test_env
        if "module_no" in self.request.args:
            module_no = int(self.request.args["module_no"])
            result, module_data = control.get_api_list(module_no, self.g.user_role)
            if result is False:
                return module_data
            current_module = None
            for part in part_module:
                for module_info in part["module_list"]:
                    if module_info["module_no"] == module_no:
                        current_module = module_info
                        current_module["part_no"] = part["part_no"]
                        current_module["part_name"] = part["part_name"]
                        break
            if current_module is None:
                return "Error"
            module_env_info = []
            if "update" in self.request.args and self.request.args["update"] == "true" and new_power is True:
                module_env = current_module["module_env"]
                if module_env is not None:
                    module_env_s = module_env.split("|")
                    env_len = len(test_env)
                    for i in range(env_len-1, -1, -1):
                        env = test_env[i]
                        if "%s" % env["env_no"] in module_env_s:
                            module_env_info.append(env)
                            test_env.remove(env)
                return self.render_template("%s/Update_API_Module.html" % html_dir, part_module=part_module, api_list=module_data["api_list"],
                                       current_module=current_module, test_env=test_env,
                                       module_env_info=module_env_info)
            my_care = None
            for item in module_data["care_info"]:
                if item["user_name"] == self.g.user_name:
                    my_care = item
                    module_data["care_info"].remove(item)
                    break
            test_module_url = test_url_prefix + "/batch/"
            return self.render_template("%s/List_Module_API.html" % html_dir, part_module=part_module, api_list=module_data["api_list"],
                                   current_module=current_module, new_power=new_power,
                                   my_care=my_care, care_info=module_data["care_info"], test_module_url=test_module_url)
        return self.render_template("%s/New_API_Module.html" % html_dir, part_module=part_module, new_power=new_power,
                                    test_env=test_env)

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