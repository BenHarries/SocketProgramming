import socket
import sys
import pickle

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

# Connect the socket to the port on the server
# given by the caller

serverip = (sys.argv[1])
port = int(sys.argv[2])

server_address = (serverip, port)
print('connecting to {} port {}'.format(*server_address))
try:
    sock.connect(server_address)

except:
    print("ERROR: Port is unavailable")
    print("Specific error: ")

    sock.close()


def timeoutError():
    print("ERROR: The server timed out")
    sock.close()
    sys.exit()


def errorHandle(boardList):
    code = pickle.loads(boardList)
    if (code) == 100:
        print("ERROR: No Boards!")
        return False
    elif (code) == 101:
        print("ERROR: Not a number of a Board!")
        return False
    elif code == 102:
        print("ERROR in request")
        return False
    else:
        return True


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


try:
    message = pickle.dumps('GET_BOARDS')
    # print("SEND", message.decode())
    try:
        sock.sendall(message)
        data = sock.recv(1040)
    except:
        timeoutError()

    if not errorHandle(data):
        sock.close()

    else:
        boards = pickle.loads(data)
        counter = 0
        for board in boards:
            counter += 1
            print((str(counter) + ". " + board + "\n"))

        text = "no user message"
        while True:  # USER CANT CURRENTLY INPUT QUIT
            text = str(input('Input: \n - A board number \n - POST to post a message \n - QUIT \n')
                       )
            if text == "QUIT":
                sock.sendall(pickle.dumps("QUIT"))
                sock.close()
                print("Succesful QUIT")
                break
            elif text == "POST":
                number_of_board = str(input("Enter your Board to post to: "))
                while not RepresentsInt(number_of_board):
                    number_of_board = str(
                        input("Last board was not a number\nEnter your Board to post to: "))

                message_title = input("Enter your message title: ")
                message_content = input("Enter your message content: ")
                post_message = ["POST_MESSAGE", number_of_board,
                                message_title, message_content]

                try:
                    sock.sendall(pickle.dumps(post_message))
                    data = sock.recv(1040)
                except:
                    timeoutError()
                if not errorHandle(data):
                    continue
                else:
                    print("Succesful POST")

            elif RepresentsInt(text):
                try:
                    sock.sendall(pickle.dumps(["GET_BOARD_MESSAGES", text]))
                    data = sock.recv(1040)
                except:
                    timeoutError()

                if not errorHandle(data):
                    continue
                else:
                    print("Succesful GET_MESSAGES")

                messages = pickle.loads(data)
                print("100 Most Recent Messages...\n")
                print("e.g Message Title:Message \n")
                length = len(messages[0])
                for c in range(length):
                    print(messages[0][length - 1 - c] + ":" +
                          messages[1][length - 1 - c] + "\n")
            else:
                print("Not a command")

finally:
    sock.close()
