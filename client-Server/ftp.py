# -*- coding: utf-8 -*-
# @Time    : 10/4/2021 7:58 PM
# @File    : ftp.py
# @Software: PyCharm

from sys import argv
import argparse
from class_client import Client


class FTP(Client):
    def __init__(self):
        super(FTP, self).__init__()
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
        self.help_socket = args.help_socket
        self.list = args.list
        self.delete = args.delete
        self.create_directory = args.create_directory
        self.rename = args.rename
        self.upload = args.upload

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
    ftp_obj = FTP()
    ftp_obj.execute()
