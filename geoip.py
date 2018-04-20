import tornado.ioloop
import tornado.web
import geoip2.database
import json
import ipaddress

geoipDbPath = '/opt/geoip.supermasita.com/GeoLite2-City/GeoLite2-City.mmdb'

class ip():

    def get_geo(remote_ip):
         
         dbReader = geoip2.database.Reader(geoipDbPath)
         try:
             response = dbReader.city(remote_ip)
             return response
         except:
             raise ValueError
         finally:
             dbReader.close()

    def is_ip(remote_ip):
         # IP or not? 
         try:
             return ipaddress.IPv4Address(remote_ip)
         #except ipaddress.AddressValueError:
         except:
             raise ValueError


class jsonHandler(tornado.web.RequestHandler):

    def get(self):

         # Checking remote_ip or query string?
         if self.get_arguments('ip'):
             remote_ip = self.get_arguments('ip', strip=True)
             remote_ip = remote_ip[0]
         elif self.request.headers.get("X-Real-IP") :
             remote_ip = self.request.headers.get("X-Real-IP") 
         elif self.request.headers.get("X-Forwarded-For") :
             remote_ip = self.request.headers.get("X-Forwarded-For") 
         else:
             remote_ip = self.request.remote_ip 

         #
         user_agent = self.request.headers.get("User-Agent")

         # IP or not? 
         try:
             ip.is_ip(remote_ip)
         #except ipaddress.AddressValueError:
         except ValueError:
             self.set_status(400)
             jsonErrorMsg = { 'status': 400, 'description': 'Not a valid IP'}
             self.finish(jsonErrorMsg)
             return


         # Check if exists in DB 
         try:
             response = ip.get_geo(remote_ip)
         #except geoip2.errors.AddressNotFoundError:
         except ValueError:
             self.set_status(400)
             jsonErrorMsg = { 'status': 400, 'description': 'IP not found in GeoLite2 database1'}
             self.finish(jsonErrorMsg)
             return


         # IP info
         jsonGeoip = {}	
         jsonGeoip = vars(response)
         del jsonGeoip['raw']
         del jsonGeoip['maxmind']
      
         # Review this header workaround 
         self.set_header('Content-Type', 'application/json') 
         self.set_header('Max-age', '3600')
 
         self.write(json.dumps(jsonGeoip, default=lambda o: o.__dict__))
         

class MainHandler(tornado.web.RequestHandler):

    def get(self):

         # Checking remote_ip or query string?
         if self.get_arguments('ip'):
             remote_ip = self.get_arguments('ip', strip=True)
             remote_ip = remote_ip[0]
         elif self.request.headers.get("X-Real-IP") :
             remote_ip = self.request.headers.get("X-Real-IP") 
         else:
             remote_ip = self.request.remote_ip 

         #
         user_agent = self.request.headers.get("User-Agent")

         # IP or not? 
         try:
             ip.is_ip(remote_ip)
         #except ipaddress.AddressValueError:
         except ValueError:
             self.set_status(400)
             jsonErrorMsg = { 'status': 400, 'description': 'Not a valid IP'}
             self.finish(jsonErrorMsg)
             return


         # Check if exists in DB 
         try:
             response = ip.get_geo(remote_ip)
         #except geoip2.errors.AddressNotFoundError:
         except ValueError:
             self.set_status(400)
             jsonErrorMsg = { 'status': 400, 'description': 'IP not found in GeoLite2 database1'}
             self.finish(jsonErrorMsg)
             return


         # IP info
         jsonGeoip = {}	
         jsonGeoip = vars(response)
         del jsonGeoip['raw']
         del jsonGeoip['maxmind']
      
         # Review this header workaround 
         self.set_header('Content-Type', 'application/json') 
         self.set_header('Max-age', '3600')

         self.write(json.dumps(jsonGeoip, default=lambda o: o.__dict__))
         

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/json/.*", jsonHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
