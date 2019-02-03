FROM xe1gyq/opencv

MAINTAINER Abraham Arce "xe1gyq@gmail.com"

ARG OPENCV_VERSION=3.4.2

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

EXPOSE 5000/udp

USER user
WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
ADD --chown=1000:1000 yolo.py /home/user/
RUN /bin/bash -c 'chmod +x /home/user/yolo.py'

ENV NAME=XunanKab
ENV STREAMPORT=5000
ENV DISPLAYIP=172.17.0.1
ENV DISPLAYPORT=5100

RUN wget https://pjreddie.com/media/files/yolov2.weights
RUN wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov2.cfg
RUN wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names

ENTRYPOINT ["bash"]
#ENTRYPOINT ["/home/user/main.sh"]
#CMD [$NAME, $STREAMPORT, $DISPLAYIP, $DISPLAYPORT]
