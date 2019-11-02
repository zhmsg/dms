#! /usr/bin/env python
# coding: utf-8


class BadRequest(Exception):

    def __init__(self, key, detail=None):
        self.key = key
        self.detail = detail
