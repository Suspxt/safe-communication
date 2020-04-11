import socket
import utils

TCP_IP, TCP_PORT = utils.request_socket_info()

BUFFER_SIZE = 10

print("IP: ", TCP_IP)
print("Port: ", TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET for IPV4, SOCK_STREAM for TCP
s.bind((TCP_IP, TCP_PORT))
s.listen(1) # Queue of 1

client_s, address = s.accept()
print(f"Established connection to {address}.")
client_s.send(bytes("Connected to prosthetic-testing-server.", "utf-8"))

while True:
    chunk = client_s.recv(BUFFER_SIZE)
    if not chunk:
        print("Connection lost.")
        break
    print(chunk) #TODO remove later
    client_s.send(bytes(chunk))

client_s.close()