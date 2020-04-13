import unittest
import utils


class TestUtils(unittest.TestCase):
    def test_validate(self):
        self.assertTrue(utils.validate_IPv4('127.0.0.1'))
        self.assertTrue(utils.validate_IPv4('255.255.255.255'))
        self.assertTrue(utils.validate_IPv4('0.0.0.0'))
        self.assertFalse(utils.validate_IPv4('127.0.1'))
        self.assertFalse(utils.validate_IPv4('.0.0.0.0'))
        self.assertFalse(utils.validate_IPv4('0.0.0.0.'))
        self.assertFalse(utils.validate_IPv4('256.0.0.0'))
        self.assertFalse(utils.validate_IPv4('h.e.l.o'))

    def test_encrypt_decrypt_int(self):
        my_rsa = utils.RSA()
        encrypted = utils.encrypt(my_rsa.N, my_rsa.e, 'hello world')
        self.assertTrue('hello world', my_rsa.decrypt(encrypted))


if __name__ == '__main__':
    unittest.main()
