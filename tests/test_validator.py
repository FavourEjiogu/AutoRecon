import unittest
from autorecon.core.validator import is_valid_ipv4, is_valid_ipv6, is_valid_fqdn, is_private_ip, validate_target

class TestValidator(unittest.TestCase):
    def test_is_valid_ipv4(self):
        self.assertTrue(is_valid_ipv4("192.168.1.1"))
        self.assertTrue(is_valid_ipv4("8.8.8.8"))
        self.assertFalse(is_valid_ipv4("256.256.256.256"))
        self.assertFalse(is_valid_ipv4("not_an_ip"))

    def test_is_valid_ipv6(self):
        self.assertTrue(is_valid_ipv6("2001:4860:4860::8888"))
        self.assertFalse(is_valid_ipv6("not_an_ipv6"))
        self.assertFalse(is_valid_ipv6("192.168.1.1")) # IPv4 is not IPv6

    def test_is_valid_fqdn(self):
        self.assertTrue(is_valid_fqdn("scanme.nmap.org"))
        self.assertTrue(is_valid_fqdn("google.com"))
        self.assertFalse(is_valid_fqdn("-invalid.com"))
        self.assertFalse(is_valid_fqdn("invalid-.com"))
        
    def test_is_private_ip(self):
        self.assertTrue(is_private_ip("192.168.1.1"))
        self.assertTrue(is_private_ip("10.0.0.5"))
        self.assertTrue(is_private_ip("127.0.0.1"))
        self.assertFalse(is_private_ip("8.8.8.8"))
        
    def test_validate_target(self):
        res1 = validate_target("  192.168.1.1  ")
        self.assertTrue(res1["valid"])
        self.assertEqual(res1["type"], "ip")
        self.assertTrue(res1["private"])
        self.assertEqual(res1["target"], "192.168.1.1")
        
        res2 = validate_target("scanme.nmap.org")
        self.assertTrue(res2["valid"])
        self.assertEqual(res2["type"], "domain")
        self.assertFalse(res2["private"])
        
        res3 = validate_target("&& ping 8.8.8.8")
        self.assertFalse(res3["valid"])

if __name__ == '__main__':
    unittest.main()
