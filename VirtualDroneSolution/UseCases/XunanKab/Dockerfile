FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    #( umask 226 && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/50_user )
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN apt-get update && \
    apt install -y build-essential python-pip python-dev && \
    apt install -y python-cherrypy3 && \
    apt install -y python-matplotlib && \
    apt install -y python-pip && \
    rm -rf /var/lib/apt/lists/*
    
RUN sudo pip install pip --upgrade && \
    sudo pip install sphinx monotonic future nose mock sphinx-3dr-theme && \
    sudo pip install pymavlink && \
    sudo pip install dronekit && \
    sudo pip install dronekit-sitl -UI

EXPOSE 5760

USER user
WORKDIR /home/user

CMD ["/bin/bash"]
