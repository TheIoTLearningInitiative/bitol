FROM user/core-opencv

MAINTAINER Abraham Arce "xe1gyq@gmail.com"

ARG OPENVINO_VERSION=2018.4.420

ENV TIMEZONE America/Mexico_City

USER root

RUN apt-get update && apt-get install -y \
    cpio \
    build-essential \
    python3-pip \
    virtualenv \
    cmake \
    libpng12-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libglib2.0-dev \
    libgtk2.0-dev \
    libswscale-dev \
    libavcodec-dev \
    libavformat-dev \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base

ADD . /home/user/l_openvino_toolkit_p_$OPENVINO_VERSION

#USER user
#WORKDIR /home/user

ENTRYPOINT [ "sh" ]
#ENTRYPOINT [ "sh", "-c", "echo $HOME" ]
