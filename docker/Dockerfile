#docker run -d --network="web" -v /opt/docker-mounts/opt/geoip.supermasita.com:/opt/geoip.supermasita.com -p 8888:8888  --name="geoip" -t geoip

FROM ubuntu

ENV UPDATED "2018-04-04"

RUN apt-get update \
    && apt-get install -y git python3-pip curl unzip

RUN cd /opt/ \
    && curl https://codeload.github.com/supermasita/geoip.supermasita.com/zip/master -o master.zip \
    && unzip master.zip \
    && mv geoip.supermasita.com-master geoip.supermasita.com \
    && rm -f master.zip

RUN cd /opt/geoip.supermasita.com && pip3 install -r requirements.txt

RUN curl http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz -o /opt/geoip.supermasita.com/GeoLite2-City.tar.gz \
    && tar xf /opt/geoip.supermasita.com/GeoLite2-City.tar.gz --directory /opt/geoip.supermasita.com/ \
    && mv /opt/geoip.supermasita.com/GeoLite2-City_2* /opt/geoip.supermasita.com/GeoLite2-City \
    && rm -f /opt/geoip.supermasita.com/GeoLite2-City.tar.gz

EXPOSE 8888

CMD ["/usr/bin/python3", "/opt/geoip.supermasita.com/geoip.py"]
