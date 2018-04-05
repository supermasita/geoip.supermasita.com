import tornado.ioloop
import tornado.web
import geoip2.database
import json
import ipaddress

geoipDbPath = '/opt/geoip.supermasita.com/GeoLite2-City/GeoLite2-City.mmdb'

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
                 jsonErrorMsg = { 'status': 400, 'description': 'Not a valid IP'}
                 self.finish(jsonErrorMsg)
                 return
         else :
             checkIp = self.request.remote_ip 


         # Load DB
         dbReader = geoip2.database.Reader(geoipDbPath)

        
         # Check if exists in DB 
         try:
             response = dbReader.city(checkIp)
         except geoip2.errors.AddressNotFoundError:
             self.set_status(400)
             jsonErrorMsg = { 'status': 400, 'description': 'IP not found in GeoLite2 database'}
             self.finish(jsonErrorMsg)
             return
         finally:
             dbReader.close()


         # IP info
         jsonGeoip = {}	
         jsonGeoip = vars(response)
         del jsonGeoip['raw']
         del jsonGeoip['maxmind']
         jsonGeoip['service'] = {} 
         jsonGeoip['service']['checked_ip'] = checkIp
         jsonGeoip['service']['name'] = "geoip.supermasita.com"
         jsonGeoip['service']['description'] = "Get geo IP information based on Maxmind's GeoLite2 data."
         jsonGeoip['service']['how_to_use'] = "Connect directly to geoip.supermasita.com to check your request's IP. Use the query string '?ip=' to check any IP. Output is always JSON."
         jsonGeoip['service']['license'] = "Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).This product includes GeoLite2 data created by MaxMind, available from http://www.maxmind.com"
      
         # Review this header workaround 
         self.set_header('Content-Type', 'application/json') 
         self.finish(json.dumps(jsonGeoip, default=lambda o: o.__dict__))
         

def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
