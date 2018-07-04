#docker run -d --network="web" -v /opt/docker-mounts/opt/geoip.supermasita.com:/opt/geoip.supermasita.com -p 8888:8888  --name="geoip" -t geoip

FROM ubuntu:18.04

ENV UPDATED "2018-07-04"

RUN apt-get update && apt-get install -y gnupg

RUN echo "deb http://ppa.launchpad.net/maxmind/ppa/ubuntu bionic main" >> /etc/apt/source.list

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F44B38CE3DB1BF64B61DBD28DE1997DCDE742AFA 

RUN apt-get update \
    && apt-get install -y git python3-pip curl unzip cron geoipupdate supervisor 

RUN cd /opt/ \
    && curl https://codeload.github.com/supermasita/geoip.supermasita.com/zip/master -o master.zip \
    && unzip master.zip \
    && mv geoip.supermasita.com-master geoip.supermasita.com \
    && rm -f master.zip

RUN cd /opt/geoip.supermasita.com && pip3 install -r requirements.txt

RUN mkdir /opt/geoip.supermasita.com/GeoLite2-City/ \ 
    && /usr/bin/geoipupdate -d /opt/geoip.supermasita.com/GeoLite2-City/

COPY geoipupdate.cron /etc/cron.d/geoipupdate

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf 

EXPOSE 8888

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
