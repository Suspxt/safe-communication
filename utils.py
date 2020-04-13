import random
import binascii

def validate_IPv4(address):
    if isinstance(address, str):
        vals = address.split('.')
        for str_val in vals:
            try:
                val = int(str_val)
            except ValueError:
                return False
            if val > 0 and str_val[0] == '0' \
               or val < 0 or val > 255:
                return False
        return len(vals) == 4
    return False


def request_socket_info():
    tcp_ip = ''
    tcp_port = 0
    while not validate_IPv4(tcp_ip):
        tcp_ip = input("Enter the IPv4 address, or enter nothing for localhost: ") or '127.0.0.1'
    while tcp_port < 49152 or tcp_port > 65535:
        tcp_port = input("Enter the TCP port (from 49152 to 65535, exclusive), or enter nothing for 55555: ") or '55555'
        try:
            tcp_port = int(tcp_port)
        except ValueError:
            tcp_port = 0
    return tcp_ip, tcp_port

def is_prime(number, test_count):
    """
    Uses the Miller-Rabin test for primality to determine, through TEST_COUNT
    tests, whether or not NUMBER is prime.
    """
    if number == 2 or number == 3:
        return True
    if number <= 1 or number % 2 == 0:
        return False
    d = 0
    r = number - 1
    while r % 2 == 1:
        d += 1
        r //= 2
    for _1 in range(test_count):
        a = random.randrange(2, number - 1)
        x = pow(a, r, number)
        if x != 1 and x != number - 1:
            for _2 in range(d):
                x = (x ** 2) % number
                if x == 1:
                    return False
                if x == number - 1:
                    break
            if x != number - 1:
                return False
    return True


def generate_large_prime(bits, tests):
    """
    Generates a very large prime number of BITS bits.
    """
    candidate = 0
    while not is_prime(candidate, tests):
        candidate = random.randrange(1 + 2 ** (bits - 1), 2 ** bits, 2)
    return candidate


def generate_coprime(lower, upper, value):
    """
    Generates a number between LOWER (inclusive) and UPPER (exclusive) that is
    coprime to VALUE.
    """
    coprimes = [i for i in range(lower, upper) if egcd(i, value)[0] == 1]
    if len(coprimes) == 0:
        i = upper
        while True:
            if egcd(i, value)[0] == 1:
                return i
            i += 1
    return random.choice(coprimes)


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
    encoded = int(binascii.hexlify(message.encode('utf-8')), 16)
    return pow(encoded, e, N)

encrypt(123123, 23, 'hello')

class RSA:

    def __init__(self):
        """
        Chooses p, q as 15-bit prime numbers
        """
        self.p = generate_large_prime(512, 512)
        self.q = generate_large_prime(512, 512)
        coprime = (self.p - 1) * (self.q - 1)
        self.e = generate_coprime(2, 100, coprime)
        self.N = self.p * self.q
        _, self.d, _ = egcd(self.e, coprime)
        self.d %= coprime

    def decrypt(self, message):
        decrypted = pow(message, self.d, self.N)
        decrypted = binascii.unhexlify(hex(decrypted)[2:].encode('ascii'))
        return decrypted.decode('utf-8')

    def public_key(self):
        return self.N, self.e

