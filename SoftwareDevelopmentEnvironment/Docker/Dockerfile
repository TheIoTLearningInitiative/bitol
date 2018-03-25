FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV DEBIAN_FRONTEND noninteractive

RUN     apt-get update && \
        apt-get -y upgrade && \
        apt-get install -y tightvncserver && \
        apt-get install -y --no-install-recommends ubuntu-desktop && \
        apt-get install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal

CMD ["bash"]
