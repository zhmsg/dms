#! /usr/bin/env python
# coding: utf-8

#  __author__ = 'meisanggou'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if sys.version_info <= (2, 7):
    sys.stderr.write("ERROR: dms requires Python Version 2.7 or above.\n")
    sys.stderr.write("Your Python Version is %s.%s.%s.\n" % sys.version_info[:3])
    sys.exit(1)

name = "dms"
version = "2.0"
url = "https://github.com/zhmsg/dms"
license = "MIT"
author = "meisanggou"
short_description = "dms"
long_description = """dms"""
keywords = "dms"
install_requires = ["six", "werkzeug", "flask"]

entry_points = {'console_scripts': [
    # 'json-merge=jingyun_cli.json.cli:json_merge',
]}

packages = ["dms", "dms/objects"]

setup(name=name,
      version=version,
      author=author,
      author_email="zhou5315938@163.com",
      url=url,
      packages=packages,
      license=license,
      description=short_description,
      long_description=long_description,
      keywords=keywords,
      install_requires=install_requires,
      entry_points=entry_points
      )
