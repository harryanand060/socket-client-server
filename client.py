import socket
import os
import time
from sys import argv
import argparse

script_name = str(argv[0])
print(script_name)
parser = argparse.ArgumentParser(prog=script_name)
parser.add_argument('-ip', required=True)
parser.add_argument('-file', required=True)
#parser.add_argument('-file_source', required=True)
args, unknown = parser.parse_known_args()
print(args)
test_interface = args.ip
file = args.file
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

file_size = os.path.getsize(file)

#send the file details to the client
sock.send(file.encode())
sock.send(str(file_size).encode())
#open and read the file
with open(file, "rb") as file:
    c = 0

    # starting time capture
    start_time = time.time()

    #running the file untill this loop
    while c <= file_size:
        data = file.read(1024)
        if not (data):
            break
        sock.sendall(data)
        c += len(data)

    # end time capture
    end_time = time.time()

print("file transfer complete, total time", end_time - start_time)


#closing the socket
sock.close()

