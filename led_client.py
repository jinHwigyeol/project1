#!/usr/bin/python3
import socket
import sys

server_IP = 'localhost' # 서버 IP
server_port = 10001
buff_size = 128

#command = input("Enter command: ")
if len(sys.argv) != 2:
    print("insufficient args")
    sys.exit(1)

command = sys.argv[1]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (server_IP, server_port)
sock.connect(server_addr)

try:
    sock.sendall(command.encode())
    result = sock.recv(buff_size)
    print("Received form server: {}".format(result.decode()))
except Exception as e:
    print("Exception: {}".format(str(e)))

sock.close()