import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server
# given by the caller

serverip = (sys.argv[1])
port = int(sys.argv[2])

server_address = (serverip, port)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    message = b'GET_BOARDS'
    print('sending {!r}'.format(message))
    sock.sendall(message)
    data = sock.recv(70)
    print('received {!r}'.format(data))
    text = input("Enter your Board of Choice: ")
    print(type(text))
    sock.sendall(text.encode())

finally:
    sock.close()