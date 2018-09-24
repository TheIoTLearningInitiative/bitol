FROM ubuntu:16.04

MAINTAINER Abraham Arce "xe1gyq@gmail.com"

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

RUN apt-get -y update
RUN apt-get -y install ipython python-opencv python-scipy python-numpy python-setuptools python-pip python-pygame
RUN pip install https://github.com/sightmachine/SimpleCV/zipball/master
RUN pip install svgwrite

CMD ["/bin/bash"]
