FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ENV TIMEZONE America/Mexico_City
ENV ENVIRONMENTAL /etc/profile
ENV USER root


ENV DEBIAN_FRONTEND noninteractive

ENV PATH=$PATH:$PATH/ardupilot/Tools/autotest
ENV PATH=/usr/lib/ccache:$PATH
ENV LATITUDE=20.6546009
ENV LONGITUDE=-103.3915602
ENV ALTTITUDE=10

RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y git && \
    apt-get install -y screen && \
    apt-get install -y python-matplotlib python-serial python-wxgtk3.0 python-wxtools python-lxml && \
    apt-get install -y python-scipy python-opencv ccache gawk git python-pip python-pexpect && \
    apt-get install -y python-pip && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install pip --upgrade && \
    pip install future pymavlink MAVProxy

RUN groupadd user && \
    useradd -u 1000 -g user -s /bin/bash -d /home/user -m user && \
    #( umask 226 && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/50_user )
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

EXPOSE 10000-10001
EXPOSE 14550-14559

ADD --chown=1000:1000 main.sh /home/user/
RUN mkdir /home/user/ardupilot/
COPY --chown=1000:1000 ardupilot/ /home/user/ardupilot/

RUN echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> $ENVIRONMENTAL && \
    echo 'export PATH=/usr/lib/ccache:$PATH' >> $ENVIRONMENTAL

USER user

#RUN git clone git://github.com/ArduPilot/ardupilot.git && \
#    cd /home/user/ardupilot && \
#    git submodule update --init --recursive && \
#    PATH=$PATH:$HOME/ardupilot/Tools/autotest && \
#    PATH=/usr/lib/ccache:$PATH && \
#    sim_vehicle.py -v ArduCopter
#    . /etc/profile && sim_vehicle.py -w

WORKDIR /home/user
#VOLUME /home/user/ardupilot

#CMD ["/home/user/main.sh"]
ENV SIM_OPTIONS "--out=udpout:docker.for.mac.localhost:14559"
ENV SPEEDUP 1
ENTRYPOINT . $ENVIRONMENTAL && \
           sim_vehicle.py --speedup=$SPEEDUP $SIM_OPTIONS

#SYS_ID=$1
#GCS_HOST=$2
#GCS_PORT=$3
#SCRIPTS_DIR=$(cd $(dirname $(which $0)); pwd)
# docker run --rm -it 
#            -v $SCRIPTS_DIR:/external 
#	     -e "SIM_OPTIONS=--out=udpout:$GCS_HOST:$GCS_PORT 
#	     -m 
#	     --target-system=$SYS_ID" 
#	     --entrypoint "/external/entryPoint.sh" 
#	     gmyoungbloodparc/ardupilot-sitl 
#	     $SYS_ID
	   
