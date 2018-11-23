FROM ubuntu:16.04

MAINTAINER Abraham "xe1gyq@gmail.com"

ARG GSTREAMER_VERSION=4.0.0-beta

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

RUN apt-get update && apt-get install -y sudo
#RUN apt-get update && apt-get install -y sudo build-essential cmake pkg-config libjpeg8-dev \
#    libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev \
#    libswscale-dev libv4l-0 libv4l-dev libxvidcore-dev libx264-dev \
#    libatlas-base-dev gfortran wget unzip python-dev python-numpy \
#    libtbb2 libtbb-dev libjpeg-dev libpng-dev libjasper-dev libdc1394-22-dev \
#    libgtk-3-dev python3.5-dev git python3-pip python3-testresources \
#    libcanberra-gtk-module nano

RUN apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc \
    gstreamer1.0-tools libgstreamer-plugins-base1.0-dev && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5000

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER user
WORKDIR /home/user

CMD ["/bin/bash"]
