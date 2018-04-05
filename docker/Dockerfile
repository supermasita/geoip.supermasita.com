FROM ubuntu

ENV UPDATED "2018-04-04"

RUN apt-get install -y pip3-python

RUN git clone git@github.com:supermasita/geoip.supermasita.com.git /opt/geoip.supermasita.com

RUN cd /opt/geoip.supermasita.com && pip3 install -r requirements.txt

RUN curl http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -o /opt/geoip.supermasita.com/GeoLite2-City.tar.gz 
    && tar xf /opt/geoip.supermasita.com/GeoLite2-City.tar.gz --directory /opt/geoip.supermasita.com/
    && mv /opt/geoip.supermasita.com/GeoLite2-City_2* /opt/geoip.supermasita.com/GeoLite2-City
    && rm -f /opt/geoip.supermasita.com/GeoLite2-City.tar.gz


