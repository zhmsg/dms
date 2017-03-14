#! /usr/bin/env python
# coding: utf-8
__author__ = 'ZhouHeng'

from time import time
import requests
from Tools.Mysql_db import DB


class DyUpsManager(object):
    def __init__(self, address):
        self.address = str(address).rstrip("/")
        self.detail_url = self.address + "/detail"
        self.list_url = self.address + "/list"
        self.get_url = self.address + "/upstream"
        self.update_url = self.address + "/upstream"
        self.delete_url = self.address + "/upstream"
        self.db = DB()
        self.t_server = "upstream_server_nodes"

    def select_server_nodes(self, upstream_name):
        cols = ["upstream_name", "server_ip", "server_port", "adder", "insert_time"]
        db_items = self.db.execute_select(self.t_server, where_value=dict(upstream_name=upstream_name), cols=cols)
        return db_items

    def insert_server_nodes(self, upstream_name, server_ip, server_port, adder):
        kwargs = dict(upstream_name=upstream_name, server_ip=server_ip, server_port=server_port, adder=adder)
        kwargs["insert_time"] = int(time())
        l = self.db.execute_insert(self.t_server, args=kwargs, ignore=True)
        return l

    def delete_server_nodes(self, upstream_name, server_ip, server_port, adder):
        where_value = dict(upstream_name=upstream_name, server_ip=server_ip, server_port=server_port, adder=adder)
        l = self.db.execute_delete(self.t_server, where_value=where_value)
        return l

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
        if resp.status_code == 404:
            return False, "不存在"
        r_server = []
        if resp.status_code == 200:
            r_server.extend(resp.text.split("\n"))
        upstream_server = []
        for item in r_server:
            if item.startswith("server"):
                upstream_server.append(item)
        return True, upstream_server

    def get_server_list(self, upstream_name):
        exec_r, upstream_server = self.get_upstream(upstream_name)
        if exec_r is False:
            return exec_r, upstream_server
        server_nodes = self.select_server_nodes(upstream_name)
        r_list = []
        for item in upstream_server:
            r_list.append(dict(server_item=item, status=1, status_desc="服务中"))
        for item in server_nodes:
            server_item = "server %s:%s" % (item["server_ip"], item["server_port"])
            if server_item not in upstream_server:
                item.update(dict(server_item=server_item, status=0, status_desc="未添加"))
                r_list.append(item)
            else:
                index = upstream_server.index(server_item)
                r_list[index].update(item)
        return True, r_list

    def _update_upstream(self, upstream_name, server_list):
        if len(server_list) < 1:
            return False, "请至少保留一个节点"
        body = ""
        for item in server_list:
            body += item + ";"
        resp = requests.post(self.update_url + "/%s" % upstream_name, data=body)
        return True, resp.text

    def add_upstream(self, upstream_name, server_ip, server_port):
        exec_r, server_list = self.get_upstream(upstream_name)
        if exec_r is False:
            return exec_r, server_list
        add_item = "server %s:%s" % (server_ip, server_port)
        for item in server_list:
            if item == add_item:
                return True, "已存在"
        server_list.append(add_item)
        return self._update_upstream(upstream_name, server_list)

    def remove_upstream(self, upstream_name, server_ip, server_port):
        exec_r, server_list = self.get_upstream(upstream_name)
        if exec_r is False:
            return exec_r, server_list
        server_item = "server %s:%s" % (server_ip, server_port)
        if server_item not in server_list:
            return False, "不存在"
        server_list.remove(server_item)
        return self._update_upstream(upstream_name, server_list)


if __name__ == "__main__":
    dm = DyUpsManager("http://local.dyups.gene.ac")
    # c = dm.detail_upstream()
    # dm.list_upstream()
    dm.get_upstream(("apicluster2"))
    dm.get_upstream(("apicluster"))
