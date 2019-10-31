#! /usr/bin/env python
# coding: utf-8

from dms.utils.singleton import Singleton

from dms.objects.resources.api_help import ApiHelpManager


class ResourcesManager(Singleton):

    def __init__(self):
        self.objects = dict()
        self.load_objects()

    def load_objects(self):
        api_help = ApiHelpManager()
        self.objects[api_help.name] = api_help

    def get_object_manager(self, name):
        return self.objects.get(name)
