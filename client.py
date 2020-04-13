import socket
import utils

TCP_IP, TCP_PORT = utils.request_socket_info()
BUFFER_SIZE = 1024

SHOW_CODES = False
KEY_IDENTIFIER = "Public key: "

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
received = s.recv(BUFFER_SIZE)
key = received.decode('utf-8')
print("received: \n", received)
key = key[(key.find(KEY_IDENTIFIER) + len(KEY_IDENTIFIER)):]
key = key.strip("()")
key = key.split(", ")
N = int(key[0])
e = int(key[1])
print("Enter '/close' to close the socket.")
print("Enter '/toggleShow' to toggle showing your encrypted messages.")
while True:
    message = input()
    if message == '/close':
        print("Closing socket...")
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        break
    elif message == "/toggleShow":
        SHOW_CODES = not SHOW_CODES
        continue
    if len(message) == 0:
        message = '[]'
    else:
        message = '[' + str(utils.encrypt(N, e, message)) + ']'
    if SHOW_CODES:
        print(message)
    try:
        s.send(bytes(message, "utf-8"))
    except ConnectionAbortedError:
        print("Connection lost. Last two messages not sent.")
        s.close()
        break
