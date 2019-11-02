#! /usr/bin/env python
# coding: utf-8

from functools import wraps

from dms.utils.singleton import Singleton


def _verify_policies(policies):

    def _verify(f):
        @wraps(f)
        def _wrap(*args, **kwargs):
            r = f(*args, **kwargs)
            return r
        return _wrap
    return _verify


class PolicyManager(Singleton):

    def __init__(self):
        pass

    @classmethod
    def verify_policy(cls, policies):
        return _verify_policies(policies)


if __name__ == "__main__":
    class A(object):

        @PolicyManager.verify_policy(["abc"])
        def test(self, a, b, *args, **kwargs):
            print(a)
            print(b)
    a = A()
    print(a.test)
    a.test(1, 2)
