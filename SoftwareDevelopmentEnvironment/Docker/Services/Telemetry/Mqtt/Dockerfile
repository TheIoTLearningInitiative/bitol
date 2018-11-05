FROM user/core-dronekit

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile


RUN pip install paho-mqtt ppretty pyserial

USER user
WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
ADD --chown=1000:1000 mqtt.py /home/user/
RUN /bin/bash -c 'chmod +x /home/user/mqtt.py'

EXPOSE 5762/tcp
EXPOSE 5763/tcp
EXPOSE 5764/tcp

ENV CONNECTION=tcp:172.17.0.2:5764
ENV VEHICLEID=1

ENTRYPOINT ["/home/user/main.sh"]
CMD [$CONNECTION, $VEHICLEID]
