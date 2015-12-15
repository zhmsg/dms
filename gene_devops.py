#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from fabric.api import *

env.hosts = ["gene.ac"]


def test():
    print("hello world")


def deploy_test():
    with cd("/home/msg/BioMed"):
        run("pwd")
        run("sh stop.sh")
        run("git stash")
        run("git pull")
        run('find -name "*.log" | xargs rm -rf')
        run('ssh service "sh /home/msg/BioMed/restart_service.sh"')
        run("sh start_api.sh && sleep 1")


def deploy_dms():
    with cd("/home/msg/dms"):
        run("sh stop_web.sh")
        run('find -name "*.log" | xargs rm -rf')
        run("git pull")
        run("sh start_web.sh && sleep 1")
        run("cat Web/msg_web.log")
