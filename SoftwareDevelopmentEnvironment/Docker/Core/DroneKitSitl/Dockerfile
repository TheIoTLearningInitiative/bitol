FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt install -y sudo && \
    apt install -y python-pip python-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pip && \
    pip install pyserial && \
    pip install dronekit && \
    pip install dronekit-sitl -UI

EXPOSE 5760

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    adduser user dialout

USER user
WORKDIR /home/user

ENV VEHICLEID=1
ENV LATITUDE=20.6546009
ENV LONGITUDE=-103.3915602
ENV ALTITUDE=10
ENV YAW=0

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
RUN /home/user/main.sh $VEHICLEID $LATITUDE $LONGITUDE $ALTITUDE $YAW &

ENTRYPOINT ["/home/user/main.sh"]
CMD [$VEHICLEID, $LATITUDE, $LONGITUDE, $ALTITUDE, $YAW]
