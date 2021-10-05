# -*- coding: utf-8 -*-
# @Time    : 9/30/2021 3:42 PM
# @Author  : Tabassum Jahan
# @File    : client.py
# @Software: PyCharm

import socket
import os
import time
from sys import argv
import argparse


class Client:

    def __init__(self):
        script_name = str(argv[0])
        # print(script_name)
        parser = argparse.ArgumentParser(prog=script_name)
        parser.add_argument('-ip', required=True, help="Server IP ")
        parser.add_argument('-port', required=True, help="Server Port")
        parser.add_argument('-hs', '--help_socket', action="store_true", help="help for all the commands")
        parser.add_argument('-ls', '--list', nargs="?", const=True, help="list command for current directory")
        parser.add_argument('-d', '--delete', action="store_true", help="delete command also pass -f file source")
        parser.add_argument('-cd', '--create_directory', action="store_true",
                            help="create directory command also pass -f file source")
        parser.add_argument('-u', '--upload', action="store_true", help="upload file command also pass -f file source")
        parser.add_argument('-f', '--file', help="file source command")
        parser.add_argument('-rn', '--rename', action="store_true",
                            help="Rename Command also pass -of old file name and -nf new file name")
        parser.add_argument('-of', '--old_file', help="old file name command")
        parser.add_argument('-nf', '--new_file', help="new file name command")

        args, unknown = parser.parse_known_args()
        self.ip = args.ip  # self.ip = socket.gethostbyname(socket.gethostname())
        self.port = int(args.port)
        self.addr = (self.ip, self.port)
        self.size = 1024
        self.format = "utf-8"
        self.server_data_path = "server_data"
        self.help_socket = args.help_socket
        self.list = args.list
        print(self.list)
        self.delete = args.delete
        self.create_directory = args.create_directory
        self.rename = args.rename
        self.upload = args.upload
        self.file_source = None
        self.old_file = None
        self.new_file = None

        if self.delete or self.create_directory or self.upload:
            if not args.file:
                parser.error('Please provide file argument -f')
            else:
                self.file_source = args.file

        if self.rename:
            if not args.old_file or not args.new_file:
                parser.error('Please provide old and new file name for rename -of & -nf')
            else:
                self.old_file = args.old_file
                self.new_file = args.new_file

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect(self.addr)

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

    def command_list(self):
        if self.help_socket:
            self.help("HELP")
        elif self.list:
            self.list_command("SHOW_DIR")
        elif self.create_directory:
            self.make_dir_command("CREATE_DIR", self.file_source)
        elif self.delete:
             self.delete_command("DELETE", self.file_source)
        elif self.rename:
            self.rename_command("RENAME", self.old_file, self.new_file)
        elif self.upload:
            self.upload_command("UPLOAD", self.file_source)
        # else:
        #     self.close()

    def execute(self):
        self.connect()
        while True:
            data = self.client.recv(self.size).decode(self.format)
            cmd, msg = data.split("@")
            if cmd == "DISCONNECTED":
                print(f"[SERVER]: {msg}")
                break
            elif cmd == "OK":
                print(f"{msg}")
            elif cmd == "response":
                print(f"{msg}")
                break

            self.command_list()

        self.client.close()


if __name__ == "__main__":
    client_obj = Client()
    client_obj.execute()

