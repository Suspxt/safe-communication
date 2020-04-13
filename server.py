import socket
import utils

TCP_IP, TCP_PORT = utils.request_socket_info()
BUFFER_SIZE = 1024

print("Generating an RSA Scheme...")
my_rsa = utils.RSA()
public_key = my_rsa.public_key()

print("IP: ", TCP_IP)
print("Port: ", TCP_PORT)
print("Public key: ", str(public_key))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

client_s, address = s.accept()
print(f"Established connection to {address}.")
client_s.send(bytes("Connected to server. Public key: " + str(public_key), "utf-8"))


def separate_messages(chunk):
    start = chunk.find('[') + 1
    end = chunk.find(']')
    if end == -1:
        return chunk
    return chunk[start:end], chunk[end + 1:]


carry_over = ""
while True:
    chunk = client_s.recv(BUFFER_SIZE)
    if not chunk:
        print("Connection lost.")
        break
    chunk = str(chunk, 'utf-8')
    chunk = carry_over + chunk
    message, carry_over = separate_messages(chunk)
    if len(message) == 0:
        print("")
        continue
    print(my_rsa.decrypt(int(message)))

client_s.close()
