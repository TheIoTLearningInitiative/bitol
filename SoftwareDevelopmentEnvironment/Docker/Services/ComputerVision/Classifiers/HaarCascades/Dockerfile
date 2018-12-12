FROM user/core-opencv

MAINTAINER Abraham Arce "xe1gyq@gmail.com"

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

EXPOSE 5000
EXPOSE 5200

USER user
WORKDIR /home/user

ADD --chown=1000:1000 main.sh /home/user/
RUN /bin/bash -c 'chmod +x /home/user/main.sh'
ADD --chown=1000:1000 haarcascades.py /home/user/
RUN /bin/bash -c 'chmod +x /home/user/haarcascades.py'

ENV NAME=XunanKab
ENV STREAMPORT=5000
ENV DISPLAYIP=172.17.0.1
ENV DISPLAYPORT=5200

ENTRYPOINT ["bash"]
#ENTRYPOINT ["/home/user/main.sh"]
#CMD [$NAME, $STREAMPORT, $DISPLAYIP, $DISPLAYPORT]
