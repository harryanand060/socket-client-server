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
# file_name = input("File Name:")
# file_size = os.path.getsize(file_name)

file_name = client.recv(100).decode()
file_size = client.recv(100).decode()

# #send the file details to the client
# client.send(file_name.encode())
# client.send(str(file_size).encode())

#open and write the file.
with open("./recv/" + file_name, "wb") as file:
    c = 0

    #starting time capture
    start_time = time.time()

    #will run the loop till all the files is recieved.
    while c <= int(file_size):
        data = client.recv(1024)
        if not(data):
            break
        file.write(data)
        c += len(data)
    #ending the time captured
    end_time = time.time()

print("File transfer complete. Total time: ", end_time - start_time)

#closing the Socket
sock.close()

os.path.abspath()