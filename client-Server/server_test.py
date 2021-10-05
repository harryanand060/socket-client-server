
import os
import socket
import threading
import shutil
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        if cmd == "SHOW_DIR":
            file_path= os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(file_path) == 0:
                send_data += "The server directory is empty"
            else:
                for root, dirs, files in os.walk("./server_data/"):
                    path = root.split(os.sep)
                    send_data += (len(path) - 1) * '---' + os.path.basename(root) + "\n"
                    for file in files:
                        send_data +=len(path) * '---'+ file + "\n"
                #send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            print(filepath)
            print(text)
            with open(filepath, "wb") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    #os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    path = f"{SERVER_DATA_PATH}/{filename}"
                    isdir = os.path.isdir(path)
                    if isdir is True:
                        try:
                            shutil.rmtree(path)
                            # os.rmdir(path)
                            print("Directory have been removed successfully")
                        except FileExistsError:
                            print("No directory find by this name")

                    else:
                        try:
                            os.remove(path)
                            print("File have been removed successfully")
                        except:
                            print("No file find by this name")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break

        elif cmd == "RENAME":
            #for root, dirs, files in os.walk("./server_data/"):

            send_data = "OK@"
            path = f"{SERVER_DATA_PATH}/"
            old_file_name = path + data[1]
            new_file_name = path + data[2]

            os.rename(old_file_name, new_file_name)
            send_data += " Renamed successfully"
            conn.send(send_data.encode(FORMAT))


        elif cmd == "CREATE_DIR":
            files = os.listdir(SERVER_DATA_PATH)
            try:
                send_data = "OK@"
                filename = data[1]
                print(filename)

                #path = f"{SERVER_DATA_PATH}/{filename}"
                path = f"{SERVER_DATA_PATH}"
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

            conn.send(send_data.encode(FORMAT))


        elif cmd == "HELP":
            data = "OK@"
            data += "SHOW_DIR: Show  all the directory of the server.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "CREATE_DIR: Create file/folder on server.\n"
            data += "RENAME: Rename the file/folder name.\n"
            data += "HELP: List all the commands."

            conn.send(data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()