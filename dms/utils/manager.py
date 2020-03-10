#! /usr/bin/env python
# coding: utf-8

from dms.utils.singleton import Singleton

from dms.objects.resources.api_help import ApiHelpManager
from dms.objects.resources.link import ShortLinkManager
from dms.objects.resources.param_format import ParamFormatManager
from dms.objects.resources.user_policies import UserPoliciesManager
from dms.objects.web_config import WebConfig


class Explorer(Singleton):

    def __init__(self):
        self._objects = dict()
        self._modules = dict()
        self.load_objects()
        self.config = WebConfig()

    @property
    def objects(self):
        return self._objects

    @property
    def modules(self):
        return self._modules

    def manager_modules(self, policies):
        _manager_modules = dict()
        for name, module in self._modules.items():
            if name not in policies:
                continue
            manager_role = "manager"
            if manager_role in policies[name]:
                _manager_modules[name] = module
        return _manager_modules

    def _add_object(self, o):
        if o.name in self._objects:
            raise RuntimeError("Duplicate object name %s" % o.name)
        self._objects[o.name] = o
        _m = o.get_modules_desc()
        if _m:
            self._modules[o.name] = _m

    def load_objects(self):
        api_help = ApiHelpManager()
        link_man = ShortLinkManager()
        up_man = UserPoliciesManager()
        pf_man = ParamFormatManager()
        self._add_object(api_help)
        self._add_object(link_man)
        self._add_object(up_man)
        self._add_object(pf_man)

    def get_object_manager(self, name):
        return self._objects.get(name)
