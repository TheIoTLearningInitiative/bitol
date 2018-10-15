FROM xe1gyq/simplecv

MAINTAINER Abraham Arce "xe1gyq@gmail.com"

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

RUN apt-get -y update
RUN apt-get -y install ffmpeg

EXPOSE 5000

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    adduser user video

USER user
WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
ADD --chown=1000:1000 timelapse.py /home/user/
RUN /bin/bash -c 'chmod +x /home/user/timelapse.py'

ENV FRAMES=30
ENV INTERVAL=1
ENV FPS=15

ENTRYPOINT ["/home/user/main.sh"]
CMD [$FRAMES, $INTERVAL, $FPS]
