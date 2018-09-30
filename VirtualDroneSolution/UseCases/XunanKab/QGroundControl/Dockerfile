FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt install -y sudo && \
    apt install -y wget bzip2 libsdl2-dev libgstreamer1.0-0 && \
    rm -rf /var/lib/apt/lists/*

#RUN pip install pip && \
#    pip install pyserial && \
#    pip install dronekit && \
#    pip install dronekit-sitl -UI

EXPOSE 5760

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    adduser user dialout

USER user
WORKDIR /home/user

RUN wget https://s3-us-west-2.amazonaws.com/qgroundcontrol/latest/QGroundControl.tar.bz2 && \
    tar xvf QGroundControl.tar.bz2 && \
    cd qgroundcontrol

WORKDIR /home/user/qgroundcontrol
RUN ls
#RUN ./qgroundcontrol-start.sh

CMD ["/bin/bash"]
