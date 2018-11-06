FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile

ENV DEBIAN_FRONTEND noninteractive

ENV PATH=$PATH:$PATH/ardupilot/Tools/autotest
ENV PATH=/usr/lib/ccache:$PATH

RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y git && \
    apt-get install -y screen && \
    apt-get install -y python-matplotlib python-serial python-wxgtk3.0 python-wxtools python-lxml && \
    apt-get install -y python-scipy python-opencv ccache gawk git python-pip python-pexpect && \
    apt-get install -y python-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pip && \
    pip install future pymavlink MAVProxy

RUN groupadd user && \
    useradd -u 1000 -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> $ENVIRONMENTAL && \
    echo 'export PATH=/usr/lib/ccache:$PATH' >> $ENVIRONMENTAL

EXPOSE 5762/tcp
EXPOSE 5763/tcp
EXPOSE 5764/tcp

USER user

WORKDIR /home/user
RUN mkdir /home/user/ardupilot/

RUN git clone git://github.com/ArduPilot/ardupilot.git && \
    cd /home/user/ardupilot && \
    git submodule update --init --recursive

RUN cd /home/user/ardupilot && \
    git submodule update --init --recursive && \
    PATH=$PATH:$HOME/ardupilot/Tools/autotest && \
    PATH=/usr/lib/ccache:$PATH && \
    sim_vehicle.py -v ArduCopter &

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
RUN /bin/bash -c 'bash /home/user/main.sh'

ENV VEHICLEID=1
ENV LATITUDE=20.6546009
ENV LONGITUDE=-103.3915602
ENV ALTITUDE=10
ENV TCPPORTA=5764
ENV UDPPORTA=14550

ENTRYPOINT ["/home/user/main.sh"]
CMD [$VEHICLEID, $LATITUDE, $LONGITUDE, $ALTITUDE, $TCPPORTA, $UDPPORTA]
