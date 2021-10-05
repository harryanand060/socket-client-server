# -*- coding: utf-8 -*-
# @Time    : 9/30/2021 3:42 PM
# @Author  : Tabassum Jahan
# @File    : client.py
# @Software: PyCharm

import socket
from sys import argv


class Client:

    def __init__(self):
        self.ip = "127.0.0.1"  # self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 22
        self.size = 1024
        self.format = "utf-8"
        self.server_data_path = "server_data"
        self.file_source = None
        self.old_file = None
        self.new_file = None
        self.list = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print((self.ip, self.port))
        self.client.connect((self.ip, self.port))

    def close(self):
        self.client.close()

    def help(self, cmd):
        self.client.send(cmd.encode(self.format))

    def logout(self, cmd):
        self.client.send(cmd.encode(self.format))

    def list_command(self, cmd):
        if isinstance(self.list, bool):
            self.client.send(cmd.encode(self.format))
        else:
            self.client.send(f"{cmd}@{self.list}".encode(self.format))

    def make_dir_command(self, cmd, *data):
        self.client.send(f"{cmd}@{data[0]}".encode(self.format))

    def delete_command(self, cmd, *data):
        self.client.send(f"{cmd}@{data[0]}".encode(self.format))

    def rename_command(self, cmd, *data):
        self.client.send(f"{cmd}@{data[0]}@{data[1]}".encode(self.format))

    def upload_command(self, cmd, *data):
        path = data[0]
        with open(f"{path}", "r") as f:
            text = f.read()
        filename = path.split("/")[-1]
        send_data = f"{cmd}@{filename}@{text}"
        self.client.send(send_data.encode(self.format))
