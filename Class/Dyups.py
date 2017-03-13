#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

import requests


class DyUpsManager(object):
    def __init__(self, address):
        self.address = str(address).rstrip("/")
        self.detail_url = self.address + "/detail"
        self.list_url = self.address + "/list"
        self.get_url = self.address + "/upstream"
        self.update_url = self.address + "/upstream"
        self.delete_url = self.address + "/upstream"

    def detail_upstream(self):
        resp = requests.get(self.detail_url)
        print(resp.text)
        return True

    def list_upstream(self):
        resp = requests.get(self.list_url)
        print(resp.text)
        return True

    def get_upstream(self, upstream_name):
        resp = requests.get(self.get_url + "/%s" % upstream_name)
        print(upstream_name)
        if resp.status_code == 404:
            return False, "不存在"
        if resp.status_code != 200:
            return True, []
        r_server = resp.text.split("\n")
        upstream_server = []
        for item in r_server:
            if item.startswith("server"):
                upstream_server.append(item)
        return True, upstream_server

    def _update_upstream(self, upstream_name, server_list):
        body = ""
        for item in server_list:
            body += item + ";"
        print(body)
        resp = requests.post(self.update_url + "/%s" % upstream_name, data=body)
        return True, resp.text

    def add_upstream(self, upstream_name, server_ip, server_port):
        exec_r, server_list = self.get_upstream(upstream_name)
        if exec_r is False:
            return exec_r, server_list
        add_item = "server %s:%s" % (server_ip, server_port)
        for item in server_list:
            if item == add_item:
                return False, "已存在"
        server_list.append(add_item)
        return self._update_upstream(upstream_name, server_list)


if __name__ == "__main__":
    dm = DyUpsManager("http://local.dyups.gene.ac")
    # c = dm.detail_upstream()
    # dm.list_upstream()
    dm.get_upstream(("apicluster2"))
    dm.get_upstream(("apicluster"))
