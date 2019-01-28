import unittest
import requests
from geoip import *


class TestStringMethods(unittest.TestCase):

    def test_is_ip_ipv4(self):
        self.assertEqual(ip.is_ip('200.143.1.121'),
                         ipaddress.IPv4Address('200.143.1.121'))

    def test_get_geo_ipv4(self):
        response = ip.get_geo('200.42.143.3')
        geoip_response = {}
        geoip_response = vars(response)
        self.assertEqual(geoip_response['country'].iso_code, "AR")

    def test_tornado_json_ipv4(self):
        geoip_response = requests.get(
            "http://127.0.0.1:8888/?ip=200.42.143.3&json")
        geoip_response = geoip_response.json()
        self.assertEqual(geoip_response['country']['iso_code'], "AR")

    def test_tornado_ipv4(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=200.42.143.3")
        self.assertRegex(geoip_response.text, "IP: <b>200.42.143.3<\/b>")

    def test_is_ip_ipv6(self):
        self.assertEqual(ip.is_ip('2001:4860:4860::8888'),
                         ipaddress.IPv6Address('2001:4860:4860::8888'))

    def test_get_geo_ipv6(self):
        response = ip.get_geo('2001:4860:4860::8888')
        geoip_response = {}
        geoip_response = vars(response)
        self.assertEqual(geoip_response['country'].iso_code, "US")

    def test_tornado_json_ipv6(self):
        geoip_response = requests.get(
            "http://127.0.0.1:8888/?ip=2001:4860:4860::8888&json")
        geoip_response = geoip_response.json()
        self.assertEqual(geoip_response['country']['iso_code'], "US")

    def test_tornado_ipv6(self):
        geoip_response = requests.get(
            "http://127.0.0.1:8888/?ip=2001:4860:4860::8888")
        self.assertRegex(geoip_response.text,
                         "IP: <b>2001:4860:4860::8888<\/b>")

    def test_tornado_ip_null(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=23.155.53.186")
        self.assertRegex(geoip_response.text, "IP: <b>23.155.53.186<\/b>")


if __name__ == '__main__':
    unittest.main()
