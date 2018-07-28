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

EXPOSE 10000-10001
EXPOSE 14550-14559

RUN echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> $ENVIRONMENTAL && \
    echo 'export PATH=/usr/lib/ccache:$PATH' >> $ENVIRONMENTAL

USER user

WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
RUN mkdir /home/user/ardupilot/

RUN git clone git://github.com/ArduPilot/ardupilot.git && \
    cd /home/user/ardupilot && \
    git submodule update --init --recursive
