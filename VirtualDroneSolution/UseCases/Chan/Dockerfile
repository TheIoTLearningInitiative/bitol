FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt install -y sudo && \
    apt install -y python-pip python-dev && \
    apt install -y git vim mplayer && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pip && \
    pip install opencv-python && \
    pip install pygame

EXPOSE 9000
EXPOSE 9617

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    adduser user dialout

USER user
WORKDIR /home/user

RUN git clone https://github.com/hanyazou/TelloPy && \
    cd TelloPy && \
    python setup.py bdist_wheel && \
    pip install dist/tellopy-*.dev*.whl --upgrade

CMD ["/bin/bash"]
