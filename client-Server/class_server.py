# -*- coding: utf-8 -*-
# @Time    : 9/30/2021 3:10 PM
# @Author  : Tabassum Jahan
# @File    : server.py
# @Software: PyCharm

import os
import socket
import threading
import shutil
import time


class Server:

    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 4456
        self.addr = (self.ip, self.port)
        self.size = 1024
        self.format = "utf-8"
        self.basewd = os.path.abspath('.')
        self.cwd = self.basewd
        self.server_data_path = os.path.dirname(os.path.abspath(__file__))
        print(self.server_data_path)
        self.thread = None

    def connect(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.addr)
        server.listen()
        print(f"[LISTENING] Server is listening on {self.ip}:{self.port}.")

        while True:
            conn, addr = server.accept()
            self.thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            self.thread.start()
            print(f"[Client  Connected]")  # {threading.activeCount() - 1}

    def handle_client(self, conn, addr):
        try:
            print(f"[NEW CONNECTION] {addr} connected.")
            conn.send("OK@Welcome to the File Server.".encode(self.format))

            while True:
                data = conn.recv(self.size).decode(self.format)
                data = data.split("@")
                cmd = data[0]

                if cmd == "SHOW_DIR":
                    self.list_directory(conn, data)
                elif cmd == "UPLOAD":
                    self.upload(conn, data)
                elif cmd == "DELETE":
                    self.delete(conn, data)
                # elif cmd == "LOGOUT":
                #     self.logout()
                elif cmd == "RENAME":
                    self.rename(conn, data)
                elif cmd == "CREATE_DIR":
                    self.create_directory(conn, data)
                elif cmd == "HELP":
                    self.help(conn)
            # print(f"[DISCONNECTED] {addr} disconnected")
            # conn.close()
        except Exception as ex:
            conn.close()

    def list_directory(self, conn, data):
        """

        :param conn:
        :return:
        """
        try:
            filepath = os.path.join(self.server_data_path, data[1])
        except IndexError:
            filepath = self.server_data_path

        list_path = os.listdir(filepath)
        send_data = "response@"

        if len(list_path) == 0:
            send_data += "The server directory is empty"
        else:
            for row in os.listdir(filepath):
                d = (os.path.isdir(os.path.join(filepath, row))) and 'D' or '-'
                send_data += f" {d} --- {row} \n"
            # for root, dirs, files in os.walk(filepath):
            #     path = root.split(os.sep)
            #     sendata += (len(path) - 1) * '---' + os.path.basename(root) + "\n"
            #     for file in files:
            #         send_data += len(path) * '---' + file + "\n"

        conn.send(send_data.encode(self.format))

    def toListItem(self, fn):
        st = os.stat(fn)
        fullmode = 'rwxrwxrwx'
        mode = ''
        for i in range(9):
            mode += ((st.st_mode >> (8 - i)) & 1) and fullmode[i] or '-'
        d = (os.path.isdir(fn)) and 'd' or '-'
        ftime = time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
        return d + mode + ' 1 user group ' + str(st.st_size) + ftime + os.path.basename(fn)

    def upload(self, conn, data):
        """

        :param conn:
        :return:
        """
        name, text = data[1], data[2]
        filepath = os.path.join(self.server_data_path, name)
        with open(filepath, "w") as f:
            f.write(text)

        send_data = "response@File uploaded successfully."
        conn.send(send_data.encode(self.format))

    def delete(self, conn, data):
        """

        :param conn:
        :param data:
        :return:
        """
        files = os.listdir(self.server_data_path)
        # print("data ",data)
        send_data = "response@"
        filename = data[1]

        if len(files) == 0:
            send_data += "The server directory is empty"
        else:
            # if filename in files:
            # os.system(f"rm {SERVER_DATA_PATH}/{filename}")
            path = f"{self.server_data_path}/{filename}"
            # print("PATH ",path)
            isdir = os.path.isdir(path)
            # print(isdir)
            if isdir is True:
                try:
                    shutil.rmtree(path)
                    # os.rmdir(path)
                    send_data += "Directory have been removed successfully"
                except FileExistsError:
                    send_data += "No directory find by this name"

            else:
                try:
                    os.remove(path)
                    send_data += "File have been removed successfully"
                except:
                    send_data += "No file find by this name"
            # send_data += "File deleted successfully."
            # else:
            #     send_data += "File not found."

        conn.send(send_data.encode(self.format))

    def logout(self):
        """

        :param conn:
        :return:
        """
        pass

    def rename(self, conn, data):
        """

        :param conn:
        :param data:
        :return:
        """
        send_data = "response@"
        path = f"{self.server_data_path}/"
        old_file_name = path + data[1]
        new_file_name = path + data[2]

        os.rename(old_file_name, new_file_name)
        send_data += " Renamed successfully"
        conn.send(send_data.encode(self.format))

    def create_directory(self, conn, data):
        """

        :param conn:
        :param data:
        :return:
        """
        files = os.listdir(self.server_data_path)
        send_data = "response@"
        try:
            filename = data[1]
            print(filename)

            # path = f"{SERVER_DATA_PATH}/{filename}"
            path = f"{self.server_data_path}"
            print(path)
            dir_str = filename.split("/")
            print(dir_str)
            for row in dir_str:
                path += f"/{row}"
                isdir = os.path.isdir(path)
                if isdir is True:
                    continue
                check_file = os.path.splitext(row)
                print(check_file)
                extension = check_file[1]
                print(extension)
                if extension:
                    with open(path, 'wb') as file:
                        pass
                else:
                    os.mkdir(path)
            send_data += "Created successfully"
        except Exception as ex:
            send_data += f"found error {ex}"

        conn.send(send_data.encode(self.format))

    def help(self, conn):
        """

        :param conn:
        :return:
        """
        data = "response@"
        data += "SHOW_DIR: Show  all the directory of the server.\n"
        data += "UPLOAD <path>: Upload a file to the server.\n"
        data += "DELETE <filename>: Delete a file from the server.\n"
        data += "LOGOUT: Disconnect from the server.\n"
        data += "CREATE_DIR: Create file/folder on server.\n"
        data += "RENAME: Rename the file/folder name.\n"
        data += "HELP: List all the commands."

        conn.send(data.encode(self.format))


if __name__ == "__main__":
    server_obj = Server()
    server_obj.connect()
