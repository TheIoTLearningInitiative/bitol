FROM xe1gyq/dronekit

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile

USER user
WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
ADD --chown=1000:1000 rtl.py /home/user/
RUN /bin/bash -c 'chmod +x /home/user/rtl.py'

ENV IPADDRESS=172.17.0.2
ENV PORT=5763
ENV VEHICLEID=1
ENV ALTITUDE=5

ENTRYPOINT ["/home/user/main.sh"]
CMD [$IPADDRESS, $PORT, $VEHICLEID, $ALTITUDE]
