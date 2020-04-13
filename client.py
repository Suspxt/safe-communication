import socket
import utils

TCP_IP, TCP_PORT = utils.request_socket_info()
BUFFER_SIZE = 1024

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
print("Enter '/show' to toggle showing your encrypted messages.")

show = False
while True:
    message = input()
    if message == '/close':
        break
    elif message == "/show":
        show = not show
        continue
    message = '[' + str(utils.encrypt(N, e, message)) + ']'
    if show:
        print(message)
    s.send(bytes(message, "utf-8"))

print("Closing socket...")
s.close()
