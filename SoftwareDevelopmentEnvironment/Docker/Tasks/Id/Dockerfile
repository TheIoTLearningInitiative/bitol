FROM user/core-dronekit

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile

USER user
WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
ADD --chown=1000:1000 id.py /home/user/
RUN /bin/bash -c 'chmod +x /home/user/id.py'

ENV CONNECTION=tcp:172.17.0.2:5762
ENV VEHICLEID=1

ENTRYPOINT ["/home/user/main.sh"]
CMD [$CONNECTION, $VEHICLEID]
