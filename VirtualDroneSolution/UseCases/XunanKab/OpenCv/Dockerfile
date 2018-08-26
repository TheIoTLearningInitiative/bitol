FROM ubuntu:16.04

MAINTAINER Abraham Arce <xe1gyq@gmail.com>

ARG OPENCV_VERSION=3.4.2

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

RUN apt-get update && apt-get install -y sudo build-essential cmake pkg-config libjpeg8-dev \
    libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev \
    libswscale-dev libv4l-dev libxvidcore-dev libx264-dev \
    libatlas-base-dev gfortran wget unzip python-dev python-numpy \
    libtbb2 libtbb-dev libjpeg-dev libpng-dev libjasper-dev libdc1394-22-dev \
    libgtk-3-dev python2.7-dev python3.5-dev git python-pip python3-pip python3-testresources \
    libcanberra-gtk-module nano

RUN apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc \
    gstreamer1.0-tools libgstreamer-plugins-base1.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && pip3 install numpy

RUN wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip && \
    unzip -q $OPENCV_VERSION.zip && \
    rm -f $OPENCV_VERSION.zip

RUN wget https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip && \
    unzip -q $OPENCV_VERSION.zip && \
    rm -f $OPENCV_VERSION.zip

RUN mkdir -p /opencv-$OPENCV_VERSION/build

WORKDIR /opencv-$OPENCV_VERSION/build

RUN  cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D BUILD_PYTHON_SUPPORT=0N \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-$OPENCV_VERSION/modules \
    -D PYTHON3_EXECUTABLE=/usr/bin/python3.5 \
    -D BUILD_EXAMPLES=ON \
    -D BUILD_NEW_PYTHON_SUPPORT=ON \
    -D WITH_V4L=ON \
    -D WITH_TBB=ON \
    -D WITH_FFMPEG=ON \
    -D WITH_GPHOTO2=ON \
    -D WITH_GSTREAMER=ON \
    -D BUILD_DOCS=NO \
    -D BUILD_TESTS=NO \
    -D BUILD_PERF_TESTS=NO \
    -D BUILD_EXAMPLES=NO \
    -D BUILD_opencv_java=NO \
    -D BUILD_opencv_python2=NO \
    -D BUILD_opencv_python3=YES ..

RUN make -j$(nproc) && make install && ldconfig
RUN pip install imutils

RUN rm -rf opencv-$OPENCV_VERSION .zip opencv3.zip ~/opencv-3.4.2

EXPOSE 5000

RUN groupadd user && \
    useradd -g user -s /bin/bash -d /home/user -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER user
WORKDIR /home/user

CMD ["/bin/bash"]
