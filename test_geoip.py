import unittest
import requests
from geoip import *

class TestStringMethods(unittest.TestCase):

    def test_is_ip_ipv4(self):
        self.assertEqual(ip.is_ip('200.143.1.121'), '200.143.1.121')
    
    def test_get_geo_ipv4(self):
        response = ip.get_geo('200.42.143.3')
        geoip_response = {}
        geoip_response = vars(response)
        self.assertEqual(geoip_response['country'].iso_code, "AR")

    def test_tornado_json_ipv4(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=200.42.143.3&json")
        geoip_response = geoip_response.json()
        self.assertEqual(geoip_response['country']['iso_code'], "AR")
    
    def test_tornado_ipv4(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=200.42.143.3")
        self.assertRegex(geoip_response.text, "IP: <b>200.42.143.3<\/b>")
    
    def test_is_ip_ipv6(self):
        self.assertEqual(ip.is_ip('200.143.1.121'), '600:8801:9400:5a1:948b:ab15:dde3:61a3')
    
    def test_get_geo_ipv6(self):
        response = ip.get_geo('600:8801:9400:5a1:948b:ab15:dde3:61a3')
        geoip_response = {}
        geoip_response = vars(response)
        self.assertEqual(geoip_response['country'].iso_code, "US")

    def test_tornado_json_ipv6(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=600:8801:9400:5a1:948b:ab15:dde3:61a3&json")
        geoip_response = geoip_response.json()
        self.assertEqual(geoip_response['country']['iso_code'], "US")
    
    def test_tornado_ipv6(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=600:8801:9400:5a1:948b:ab15:dde3:61a3")
        self.assertRegex(geoip_response.text, "IP: <b>600:8801:9400:5a1:948b:ab15:dde3:61a3<\/b>")

if __name__ == '__main__':
    unittest.main()
