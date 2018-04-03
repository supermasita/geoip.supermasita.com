import tornado.ioloop
import tornado.web
import geoip2.database
import json
import ipaddress

class MainHandler(tornado.web.RequestHandler):
    def get(self):

         # Checking remote_ip or query string?
         queryIp = self.get_arguments('ip', strip=True)

         if queryIp :
             checkIp = queryIp[0]
             # IP or not? 
             try:
                 ipaddress.IPv4Address(checkIp)
             except ipaddress.AddressValueError:
                 self.set_status(400)
                 jsonObject = {}
                 jsonObject['status'] = 400
                 jsonObject['description'] = "Not a valid IP"
                 self.finish(jsonObject)
                 return
         else :
             checkIp = self.request.remote_ip 

         # Load DB
         reader = geoip2.database.Reader('./GeoLite2-City/GeoLite2-City.mmdb')
        
         # Check if exists in DB 
         try:
             response = reader.city(checkIp)
         except geoip2.errors.AddressNotFoundError:
             self.set_status(400)
             jsonObject = {}
             jsonObject['status'] = 400
             jsonObject['description'] = "IP not found in GeoLite2 database"
             self.finish(jsonObject)
             return

         # IP info	
         jsonObject = json.dumps(response, default=lambda o: o.__dict__)
         jsonObject = vars(response)
         del jsonObject['registered_country']
         del jsonObject['represented_country']
         del jsonObject['traits']
         del jsonObject['raw']
         del jsonObject['subdivisions']
         del jsonObject['_locales']
         del jsonObject['maxmind']
         jsonObject['accept_language'] = self.request.headers.get('Accept-Language')
         jsonObject['service'] = {} 
         jsonObject['service']['checked_ip'] = checkIp
         jsonObject['service']['name'] = "geoip.supermasita.com"
         jsonObject['service']['description'] = "Get geo IP information based on Maxmind's GeoLite2 data."
         jsonObject['service']['how_to_use'] = "Connect directly to geoip.supermasita.com to check your request's IP. Use the query string '?ip=' to check any IP. Output is always JSON."
         jsonObject['service']['license'] = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).This product includes GeoLite2 data created by MaxMind, available from http://www.maxmind.com"
         
         self.write(json.dumps(jsonObject, default=lambda o: o.__dict__))
         
         reader.close()

def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
