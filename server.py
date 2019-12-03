import socket
import select
import sys
import os
import pickle
import datetime


from _thread import *
import threading


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
    print('starting up on {} port {}'.format(*sock.getsockname()))
except error as e:
    print("ERROR: Port is unavailable")
    print("Specific error: " + str(e))
    sock.close()


directories = ([(name) for name in os.listdir(
    "./board") if os.path.isdir(os.path.join("./board", name))])

sock.listen(5)


def serverLog(clientIP_PORT, client_command, status):
    currentDateTime = datetime.datetime.now().strftime("%c")
    allFileName = os.path.join(os.getcwd(), 'serverLog.txt')
    try:
        serverLogFile = open(allFileName, "a+")
        serverLogFile.write(clientIP_PORT + '\t' + currentDateTime +
                            '\t' + client_command + '\t' + status + '\n')
        serverLogFile.close()
    except error as e:
        print('ERROR: serverLog error has occurred - ', e)


def threaded(connection):
    print("New Thread")
    while True:

        data = connection.recv(1040)
        data = pickle.loads(data)
        if not data:
            break
        print('received {!r}'.format(data))
        if data == 'GET_BOARDS':
            if len(directories) == 0:
                print("ERROR: No message boards defined")
                connection.send(pickle.dumps(100))
                connection.close()
                serverLog(formattedAddr, "GET_BOARDS", "Error")
                os._exit(0)
                return False
            else:
                try:
                    connection.sendall(pickle.dumps(directories))
                    serverLog(formattedAddr, "GET_BOARDS", "OK")
                except:
                    serverLog(formattedAddr, "GET_BOARDS", "Error")
        elif data == 'QUIT':
            connection.close()
            sys.exit()
            print("QUITING")
            break
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
                    files_by_date = {}
                    dt = []
                    dates = []
                    for file in desired_board_file_names:

                        print("file", file)
                        date = file[0:8]
                        time = file[9:15]
                        try:
                            files_by_date[desired_board + "/" + file] = datetime.datetime.strptime(
                                date+time, '%Y%m%d%H%M%S')
                        except:
                            print("file not correct format")
                            serverLog(formattedAddr,
                                      "GET_MESSAGES", "Error")
                            connection.sendall(pickle.dumps(101))
                            continue
                        dates.append(datetime.datetime.strptime(
                            date+time, '%Y%m%d%H%M%S'))
                    dt = list(
                        (sorted(files_by_date, key=files_by_date.get)))
                    print("files sorted by date")
                    dates = list((sorted(dates)))
                    print(dt)
                    print("\n")
                    messages = []
                    for c, file in enumerate(dt):
                        print(dates[c])
                        messages.append(open(file, "r").read())
                    connection.sendall(pickle.dumps(messages[:100]))
                    serverLog(formattedAddr, "GET_MESSAGES", "OK")
            elif command == "POST_MESSAGE":
                # ERROR HANDLING IF NOt A NUMBER INPUTTED
                try:
                    desired_board_num = int(data[1])
                    if desired_board_num > len(directories):
                        connection.sendall(pickle.dumps(101))
                    message_title = data[2].replace(" ", "_")
                    message_content = data[3]
                    desired_board_path = "./board/" + \
                        directories[desired_board_num-1]
                    print(desired_board_path + message_title+".txt")
                    print(datetime.datetime.now().strftime(
                        "%Y%m%d-%H%M%S-"))
                    f = open(desired_board_path + "/" + datetime.datetime.now().strftime(
                        "%Y%m%d-%H%M%S-") +
                        message_title, "w+")
                    print(message_content, "WRITING")
                    f.write(message_content)
                    f.close()
                    print("Succesful POST")
                    serverLog(formattedAddr, "POST_MESSAGE", "OK")
                    connection.sendall(pickle.dumps("All Good"))
                except:
                    serverLog(formattedAddr, "GET_MESSAGE", "Error")
                    print("Unsuccesful POST")
    return True
    connection.close()


while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    formattedAddr = str(client_address)[1:len(
        str(client_address)) - 1].replace(', ', ':').replace("'", '')
    print('client connected:', client_address)
    start_new_thread(threaded, (connection,))
connection.close()
