FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

ENV PATH=$PATH:$HOME/ardupilot/Tools/autotest
ENV PATH=/usr/lib/ccache:$PATH

RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y git && \
    apt-get install -y python-matplotlib python-serial python-wxgtk3.0 python-wxtools python-lxml && \
    apt-get install -y python-scipy python-opencv ccache gawk git python-pip python-pexpect && \
    apt-get install -y python-pip && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install pip --upgrade && \
    pip install future pymavlink MAVProxy

EXPOSE 14550
EXPOSE 14551

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    #( umask 226 && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/50_user )
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER user
WORKDIR /home/user

RUN git clone git://github.com/ArduPilot/ardupilot.git && \
    cd /home/user/ardupilot && \
    git submodule update --init --recursive && \
    PATH=$PATH:$HOME/ardupilot/Tools/autotest && \
    PATH=/usr/lib/ccache:$PATH && \
    sim_vehicle.py -v ArduCopter

# Script

CMD ["/bin/bash"]
