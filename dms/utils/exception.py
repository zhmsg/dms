#! /usr/bin/env python
# coding: utf-8


class BadRequest(Exception):

    def __init__(self, key, detail=None):
        self.key = key
        self.detail = detail


class ConflictRequest(Exception):

    def __init__(self, detail=None):
        self.detail = detail


class ResourceNotFound(Exception):

    def __init__(self, resource_name, resource_value):
        self.resource_name = resource_name
        self.resource_value = resource_value
