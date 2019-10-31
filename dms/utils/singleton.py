#! /usr/bin/env python
# coding: utf-8


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance
        o = object.__new__(cls)
        cls._instance = o
        return o

    @classmethod
    def get_instance(cls):
        return cls()
