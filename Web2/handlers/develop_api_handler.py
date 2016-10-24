#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from Web2 import control, BaseAuthHandler, test_url_prefix, api_url_prefix as url_prefix, http_handlers

html_dir = "API_HELP"


class APIIndexHandler(BaseAuthHandler):

    def get(self):
        self.request.args = self.request.arguments
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
                return self.render("%s/Update_API_Module.html" % html_dir, part_module=part_module, api_list=module_data["api_list"],
                                       current_module=current_module, url_prefix=url_prefix, test_env=test_env,
                                       module_env_info=module_env_info)
            my_care = None
            for item in module_data["care_info"]:
                if item["user_name"] == self.g.user_name:
                    my_care = item
                    module_data["care_info"].remove(item)
                    break
            test_module_url = test_url_prefix + "/batch/"
            return self.render("%s/List_Module_API.html" % html_dir, part_module=part_module, api_list=module_data["api_list"],
                                   current_module=current_module, url_prefix=url_prefix, new_power=new_power,
                                   my_care=my_care, care_info=module_data["care_info"], test_module_url=test_module_url)
        print("%s/New_API_Module.html" % html_dir)
        return self.render("%s/New_API_Module.html" % html_dir, part_module=part_module, url_prefix=url_prefix,
                               new_power=new_power, test_env=test_env)

http_handlers.append((url_prefix + "/", APIIndexHandler))