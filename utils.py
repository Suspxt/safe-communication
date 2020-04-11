import random
import math

def validate_IPv4(address):
    if isinstance(address, str):
        vals = address.split('.')
        for str_val in vals:
            try:
                val = int(val)
            except ValueError:
                return False
            if val > 0 and str_val[0] == '0' \
               or val < 0 or val > 255:
                return False
        return vals.len == 4
    return False

def request_socket_info():
    tcp_ip = ''
    tcp_port = 0
    while not validate_IPv4(tcp_ip):
        tcp_ip = input("Enter the IPv4 address, or enter nothing for localhost.") or '127.0.0.1'
    while tcp_port < 49152 or tcp_port > 65535:
        tcp_port = input("Enter the TCP port, or enter nothing for 55555") or '55555'
        try:
            tcp_port = int(tcp_port)
        except ValueError:
            tcp_port = 0
    return tcp_ip, tcp_port

def generate_prime(lower, upper, exclude=0):
    """
    Generates a random prime between LOWER (inclusive) and UPPER (exclusive), if
    one exists. Excludes EXCLUDE from being output if necessary. Generates an
    error if no prime exists within this range. Uses the Sieve of Eratosthenes to
    make a list of primes then chooses a random one.
    """
    included = [True for i in range(upper)]
    prime = 2
    search_range = math.ceil(upper ** 0.5)
    while prime <= search_range:
        if included[prime]:
            for i in range(prime**2, upper, prime):
                included[prime] = False
        prime += 1
    return random.choice([i for i in range(lower, upper) if included[i] and i != exclude])

def egcd(x, y):
    if y == 0:
        return x, 1, 0
    else:
        d, a, b = egcd(y, x % y)
        return d, b, a - (x // y) * b

def encrypt(N, e, message):
    """
    Returns the message encrypted by the RSA scheme with public key (N, e).
    """
    return (message ** e) % N

class RSA:

    def __init__(self):
        """
        Chooses p, q as 15-bit prime numbers
        """
        self.p = generate_prime(2**15, 2**16)
        self.q = generate_prime(2**15, 2**16, self.p)
        self.e = generate_prime(2, 20)
        self.N = self.p * self.q
        _, self.d, _ = egcd(self.e, (self.p - 1) * (self.q - 1))

    def decrypt(self, message):
        """
        Returns the decrypted MESSAGE
        """
        return (message ** self.d) % self.N
