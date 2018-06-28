import unittest
import requests
from geoip import *

class TestStringMethods(unittest.TestCase):

    def test_is_ip(self):
        self.assertEqual(ip.is_ip('200.143.1.121'), ipaddress.IPv4Address('200.143.1.121'))
    
    def test_get_geo(self):
        response = ip.get_geo('200.42.143.3')
        geoip_response = {}
        geoip_response = vars(response)
        self.assertEqual(geoip_response['country'].iso_code, "AR")

    def test_tornado_json(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=200.42.143.3&json")
        geoip_response = geoip_response.json()
        self.assertEqual(geoip_response['country']['iso_code'], "AR")
    
    def test_tornado(self):
        geoip_response = requests.get("http://127.0.0.1:8888/?ip=200.42.143.3")
        self.assertRegex(geoip_response.text, "IP: <b>200.42.143.3<\/b>")

if __name__ == '__main__':
    unittest.main()
