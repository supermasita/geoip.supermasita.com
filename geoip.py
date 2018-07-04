import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import geoip2.database
import json
import ipaddress
import os.path
import time

from datetime import datetime, timedelta
from tornado.options import define, options


# App setup
define("port", default=8888, help="run on the given port", type=int)

# DB location
geoipDbPath = os.path.join(os.path.dirname(
    __file__), '/var/lib/GeoIP/GeoLite2-City.mmdb')


class ip():

    def get_geo(remote_ip):
        dbReader = geoip2.database.Reader(geoipDbPath)
        try:
            ip.is_ip(remote_ip)
            response = dbReader.city(remote_ip)
            return response
        except:
            raise ValueError
        finally:
            dbReader.close()

    def is_ip(remote_ip):
        # IP or not?
        try:
            return ipaddress.ip_address(remote_ip)
        except:
            raise ValueError


class MainHandler(tornado.web.RequestHandler):

    def get(self):

        not_my_ip = False
        # Checking remote_ip or query string?
        if self.get_arguments('ip'):
            remote_ip = self.get_arguments('ip', strip=True)
            remote_ip = remote_ip[0]
            not_my_ip = True
        elif self.request.headers.get("X-Real-IP"):
            remote_ip = self.request.headers.get("X-Real-IP")
        else:
            remote_ip = self.request.remote_ip

        # unique caching per ip
        if not_my_ip is False:
            self.set_header('vary', remote_ip)

        # UA is retrieved and passed to template, but not currently used
        user_agent = self.request.headers.get("User-Agent")

        # Check if exists in DB
        try:
            response = ip.get_geo(remote_ip)
        except ValueError:
            self.set_status(400)
            jsonErrorMsg = {
                'status': 400, 'description': 'IP not valid or not found in GeoLite2 database'}
            self.finish(jsonErrorMsg)
            return

        # IP info
        geoip_response = {}
        geoip_response = vars(response)
        del geoip_response['raw']
        del geoip_response['maxmind']

        # Cache headers
        expires = datetime.utcnow() + timedelta(hours=1)
        expires = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.set_header('Expires', expires)
        self.set_header('Max-age', '3600')
        self.set_header('Cache-control', 'public')

        # Checking remote_ip or query string?
        if self.get_arguments('json'):
            # Make geoip_response seriable
            geoip_response = json.dumps(
                geoip_response, default=lambda o: o.__dict__)
            # Review this header workaround
            self.set_header('Content-Type', 'application/json')
            self.write(geoip_response)

        else:
            self.render('index.html',
                        not_my_ip=not_my_ip, remote_ip=remote_ip, user_agent=user_agent,
                        country_iso_code=geoip_response['country'].iso_code,
                        country_name=geoip_response['country'].name,
                        city_names_en=geoip_response['city'].name,
                        latitude=geoip_response['location'].latitude,
                        longitude=geoip_response['location'].longitude,
                        time_zone=geoip_response['location'].time_zone,
                        geoipDbMtime=time.ctime(os.path.getmtime(geoipDbPath))
                        )


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", MainHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
