import socket
import os
import time
from sys import argv
import argparse

script_name = str(argv[0])
print(script_name)
parser = argparse.ArgumentParser(prog=script_name)
parser.add_argument('-ip', required=True)
#parser.add_argument('-file_source', required=True)
args, unknown = parser.parse_known_args()
print(args)
test_interface = args.ip
#file_name = args.file_source
# host= input("Enter Host Name: ")
host= test_interface
print(host)
sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#trying to connect to socket.
try:
    sock.connect((host,22222))
    print("Connected Successfully")
except:
    print("Unable to connect")
    exit(0)

#Reciever file details from the sender/server.
file_name = sock.recv(100).decode()
file_size = sock.recv(100).decode()

#open and write the file.
with open("./recv/" + file_name, "wb") as file:
    c = 0

    #starting time capture
    start_time = time.time()

    #will run the loop till all the files is recieved.
    while c <= int(file_size):
        data = sock.recv(1024)
        if not(data):
            break
        file.write(data)
        c += len(data)
    #ending the time captured
    end_time = time.time()

print("File transfer complete. Total time: ", end_time - start_time)

#closing the socket
sock.close()
