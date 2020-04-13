import socket
import utils
import threading


TCP_IP, TCP_PORT = utils.request_socket_info()
BUFFER_SIZE = 1024
MAX_CLIENT_COUNT = 5
SHOW_CODES = False

print("Generating an RSA Scheme...")
my_rsa = utils.RSA()
public_key = my_rsa.public_key()

print("IP: ", TCP_IP)
print("Port: ", TCP_PORT)
print("Public key: ", str(public_key))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)
clients = {}

def add_new_client(client, address):
    clients[address] = client
    print(f"Established connection to {address}.")
    client.send(bytes("Connected to server. Public key: " + str(public_key), "utf-8"))
    carry_over = ""
    while True:
        chunk = client.recv(BUFFER_SIZE)
        if not chunk:
            print(f"Connection to {address} lost.")
            break
        chunk = str(chunk, 'utf-8')
        chunk = carry_over + chunk
        message, carry_over = utils.separate_messages(chunk)
        if SHOW_CODES:
            print(message)
        if len(message) == 0:
            print("")
            continue
        print(f"{address}: {my_rsa.decrypt(int(message))}")
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    del clients[address]

def accept_incoming_clients():
    print("Waiting for new clients...")
    client_count = 0
    while client_count <= MAX_CLIENT_COUNT:
        client, address = s.accept()
        client_thread = threading.Thread(target=add_new_client, args=(client, address), daemon=True)
        client_thread.start()
        client_count += 1


accepting_thread = threading.Thread(target=accept_incoming_clients, daemon=True)
accepting_thread.start()
print("Enter '/close' to close the server.")
print("Enter '/toggleShow' to toggle showing your encrypted messages.")

while True:
    command = input()
    if command == "/close":
        break
    elif command == "/toggleShow":
        SHOW_CODES = not SHOW_CODES
    else:
        print(f"Unknown command, {command}. Please try again.")

print("Closing server...")
for client in clients.values():
    client.shutdown(socket.SHUT_RDWR)
    client.close()
s.close()
