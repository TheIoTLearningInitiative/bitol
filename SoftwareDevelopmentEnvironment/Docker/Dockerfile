FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City

RUN     apt update && \
        apt -y upgrade && \
        apt install -y tightvncserver && \
        apt install -y --no-install-recommends ubuntu-desktop && \
        apt install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal

CMD ["bash"]
