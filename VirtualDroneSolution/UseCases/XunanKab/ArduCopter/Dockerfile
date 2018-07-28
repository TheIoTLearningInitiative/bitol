FROM xe1gyq/ardupilot

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile

USER root

RUN echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> $ENVIRONMENTAL && \
    echo 'export PATH=/usr/lib/ccache:$PATH' >> $ENVIRONMENTAL

USER user

WORKDIR /home/user

RUN cd /home/user/ardupilot && \
    git submodule update --init --recursive && \
    PATH=$PATH:$HOME/ardupilot/Tools/autotest && \
    PATH=/usr/lib/ccache:$PATH && \
    sim_vehicle.py -v ArduCopter
