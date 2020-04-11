import unittest
import utils

class test_utils(unittest.TestCase):
    def test_validate(self):
        self.assertTrue(utils.validate_IPv4('127.0.0.1'))
        self.assertTrue(utils.validate_IPv4('255.255.255.255'))
        self.assertTrue(utils.validate_IPv4('0.0.0.0'))
        self.assertFalse(utils.validate_IPv4('127.0.1'))
        self.assertFalse(utils.validate_IPv4('.0.0.0.0'))
        self.assertFalse(utils.validate_IPv4('0.0.0.0.'))
        self.assertFalse(utils.validate_IPv4('256.0.0.0'))
        self.assertFalse(utils.validate_IPv4('h.e.l.o'))

if __name__ == '__main__':
    unittest.main()