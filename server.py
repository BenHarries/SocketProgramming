import socket
import select
import sys
import os

HEADER_LENGTH = 10
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address given on the command line

serverip = (sys.argv[1])
port = int(sys.argv[2])

server_address = (serverip, port)
sock.bind(server_address)
print('starting up on {} port {}'.format(*sock.getsockname()))

sockets_list = [sock]

clients = {}

sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(16)
            if not data:
                break
            print('received {!r}'.format(data))
            if data == b'GET_BOARDS':
                print("ya")
                directories = ([(name) for name in os.listdir(
                    "./board") if os.path.isdir(os.path.join("./board", name))])
                counter = 0
                return_data = ""
                for i in directories:
                    counter += 1
                    return_data += (str(counter) + ". " + i + "; ")

                return_data = str.encode(return_data)
                connection.sendall(return_data)

            else:  # Need to have a condition here
                number_of_board = int(data.decode())
                print(directories[number_of_board-1])
    finally:
        connection.close()
