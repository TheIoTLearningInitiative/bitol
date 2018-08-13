FROM xe1gyq/arducopter

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile

EXPOSE 10000-10001
EXPOSE 5700-5800
EXPOSE 14550-14559

USER root

RUN echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> $ENVIRONMENTAL && \
    echo 'export PATH=/usr/lib/ccache:$PATH' >> $ENVIRONMENTAL

USER user

WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'

ENV VEHICLEID=1
ENV LATITUDE=20.6546009
ENV LONGITUDE=-103.3915602
ENV ALTITUDE=10

ENTRYPOINT ["/home/user/main.sh"]
CMD [$VEHICLEID, $LATITUDE, $LONGITUDE, $ALTITUDE]
