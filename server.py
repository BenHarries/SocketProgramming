import socket
import sys
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line

serverip = (sys.argv[1])
port = int(sys.argv[2])

server_address = (serverip, port)
sock.bind(server_address)
print('starting up on {} port {}'.format(*sock.getsockname()))
sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data == b'GET_BOARDS':
                print("ya")
                directories = ([(name) for name in os.listdir("./board") if os.path.isdir(os.path.join("./board", name))])
                counter = 0
                return_data = ""
                for i in directories:
                    counter += 1
                    return_data += (str(counter) + ". " + i + "; ")

                print(return_data)
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()