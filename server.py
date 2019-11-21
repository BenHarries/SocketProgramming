import socket
import select
import sys
import os
import pickle
import datetime


HEADER_LENGTH = 10
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address given on the command line

serverip = (sys.argv[1])
port = int(sys.argv[2])

server_address = (serverip, port)
try:
    sock.bind(server_address)
except error as e:
    print("ERROR: Port is unavailable")
    print("Specific error: " + str(e))
    portConnected = False
    serverSocket.close()
print('starting up on {} port {}'.format(*sock.getsockname()))

sock.listen(1)

directories = ([(name) for name in os.listdir(
    "./board") if os.path.isdir(os.path.join("./board", name))])

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(1040)
            data = pickle.loads(data)
            if not data:
                break
            print('received {!r}'.format(data))
            if data == 'GET_BOARDS':
                print("ya")

                if len(directories) == 0:
                    print("ERROR: No message boards defined")
                    connectionSocket.send(pickle.dumps(100))
                    serverSocket.close()
                    break
                # counter = 0
                # return_data = ""
                # for i in directories:
                #     counter += 1
                    # return_data += (str(counter) + ". " + i + "; ")

                # return_data = str.encode(return_data)

                # connection.sendall(return_data)

                connection.sendall(pickle.dumps(directories))

            else:  # Need to have a condition here
                command = data[0]
                if (command == "GET_BOARD_MESSAGES"):
                    number_of_board = int(data[1])
                    if number_of_board > len(directories):
                        connection.sendall(pickle.dumps(101))
                    else:
                        desired_board = "./board/" + \
                            directories[number_of_board-1]
                        desired_board_file_names = [
                            name for name in os.listdir(desired_board)]
                        desired_board_file_paths = [
                            open(desired_board + "/" + name, "r") for name in os.listdir(desired_board)]
                        messages = []
                        files_by_date = {}
                        dt = []
                        for file in desired_board_file_names:
                            print("file", file)
                            date = file[0:8]
                            time = file[9:15]
                            files_by_date[desired_board + "/" + file] = datetime.datetime.strptime(
                                date+time, '%Y%m%d%H%M%S')
                        dt = list(
                            reversed(sorted(files_by_date, key=files_by_date.get)))
                        print("files sorted by date")
                        print(dt)
                        print("\n")

                        for file in dt:
                            print(file)
                            messages.append(open(file, "r").read())
                        connection.sendall(pickle.dumps(messages[:100]))
                elif command == "POST_MESSAGE":
                    desired_board_num = int(data[1])
                    message_title = data[2]
                    message_content = data[3]
                    desired_board_path = "./board/" + \
                        directories[desired_board_num-1]
                    print(desired_board_path + message_title+".txt")
                    f = open(desired_board_path + "/" +
                             message_title+".txt", "w+")
                    f.write(message_content)

    finally:
        connection.close()
