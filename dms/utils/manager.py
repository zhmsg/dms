#! /usr/bin/env python
# coding: utf-8


from dms.utils.singleton import Singleton

from dms.objects.base import UnsetValue
from dms.objects.resources.api_help import ApiHelpManager
from dms.objects.resources.link import ShortLinkManager
from dms.objects.resources.param_format import ParamFormatManager
from dms.objects.resources.user_policies import UserPoliciesManager


class Explorer(Singleton):

    def __init__(self):
        self._objects = dict()
        self._modules = dict()
        self.missing_config = {}
        self.load_objects()

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

    def _add_module(self, cls):
        if cls.NAME is UnsetValue.get_instance():
            return
        _m = cls.get_modules_desc()
        if _m:
            self._modules[cls.NAME] = _m

    def load_object(self, cls):
        self._add_module(cls)
        if cls.valid() is False:
            self.missing_config[cls.NAME] = cls.missing_config()
            return
        _man = cls()
        self._add_object(_man)

    def load_objects(self):
        self.load_object(ApiHelpManager)
        self.load_object(ShortLinkManager)
        self.load_object(UserPoliciesManager)
        self.load_object(ParamFormatManager)

    def get_object_manager(self, name):
        return self._objects.get(name)
