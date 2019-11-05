#! /usr/bin/env python
# coding: utf-8


class ClientError(Exception):

    def __init__(self):
        pass


class BadRequest(ClientError):

    def __init__(self, key, detail=None):
        self.key = key
        self.detail = detail


class ConflictRequest(ClientError):

    def __init__(self, detail=None):
        self.detail = detail


class ResourceNotFound(ClientError):

    def __init__(self, resource_name, resource_value):
        self.resource_name = resource_name
        self.resource_value = resource_value


class Forbidden(ClientError):

    def __init__(self):
        pass
