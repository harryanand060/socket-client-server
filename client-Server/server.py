import socket
import os
import time

#creating the socket object
sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 22222))
sock.listen(5)
print("HOST: ", sock.getsockname())

#Accepting the connection from the client
client, addr = sock.accept()

#Getting the file details to be sent
file_name = input("File Name:")
file_size = os.path.getsize(file_name)

#send the file details to the client
client.send(file_name.encode())
client.send(str(file_size).encode())

#open and read the file
with open(file_name, "rb") as file:
    c = 0

    # starting time capture
    start_time = time.time()

    #running the file untill this loop
    while c <= file_size:
        data = file.read(1024)
        if not (data):
            break
        client.sendall(data)
        c += len(data)

    # end time capture
    end_time = time.time()

print("file transfer complete, total time", end_time - start_time)

#closing the Socket
sock.close()