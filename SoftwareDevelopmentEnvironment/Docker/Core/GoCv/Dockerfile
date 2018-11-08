FROM ubuntu:16.04

MAINTAINER Alfredo Reyes "reyes-fred@hotmail.com"

ARG OPENCV_VERSION=3.4.2

ENV TIMEZONE America/Mexico_City
ENV USER root

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /

RUN apt-get update && apt-get install -y sudo build-essential cmake pkg-config libjpeg8-dev \
    libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev \
    libswscale-dev libv4l-0 libv4l-dev libxvidcore-dev libx264-dev \
    libatlas-base-dev gfortran wget unzip python-dev python-numpy \
    libtbb2 libtbb-dev libjpeg-dev libpng-dev libjasper-dev libdc1394-22-dev \
    libgtk-3-dev python3.5-dev git python3-pip python3-testresources \
    libcanberra-gtk-module nano

RUN apt-get install -y libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc \
    gstreamer1.0-tools libgstreamer-plugins-base1.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl

RUN python3 -m pip install --upgrade pip && pip3 install numpy

RUN wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip && \
    unzip -q $OPENCV_VERSION.zip && \
    rm -f $OPENCV_VERSION.zip

RUN wget https://github.com/opencv/opencv_contrib/archive/$OPENCV_VERSION.zip && \
    unzip -q $OPENCV_VERSION.zip && \
    rm -f $OPENCV_VERSION.zip

RUN mkdir -p /opencv-$OPENCV_VERSION/build

WORKDIR /opencv-$OPENCV_VERSION/build

RUN  cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D BUILD_PYTHON_SUPPORT=0N \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-$OPENCV_VERSION/modules \
    -D PYTHON3_EXECUTABLE=/usr/bin/python3.5 \
    -D PYTHON_INCLUDE_DIR=/usr/include/python3.5 \
    -D PYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.5m.so \
    -D BUILD_EXAMPLES=YES \
    -D BUILD_NEW_PYTHON_SUPPORT=YES \
    -D WITH_LIBV4L=YES \
    -D WITH_V4L=YES \
    -D WITH_TBB=YES \
    -D WITH_FFMPEG=YES \
    -D WITH_GPHOTO2=YES \
    -D WITH_GSTREAMER=YES \
    -D BUILD_DOCS=NO \
    -D BUILD_TESTS=NO \
    -D BUILD_PERF_TESTS=NO \
    -D BUILD_EXAMPLES=NO \
    -D BUILD_opencv_java=NO \
    -D BUILD_opencv_python2=NO \
    -D BUILD_opencv_python3=YES ..

RUN make -j$(nproc) && make install && ldconfig
RUN ln -s /usr/local/lib/python3.5/site-packages/cv2.cpython-35m-x86_64-linux-gnu.so \
    /usr/local/lib/python3.5/dist-packages/cv2.so
RUN pip install imutils

#Begin: install golang
WORKDIR /
ENV GOLANG_VERSION 1.10.1
ENV GOLANG_DOWNLOAD_URL https://golang.org/dl/go$GOLANG_VERSION.linux-amd64.tar.gz
ENV GOLANG_SHA256_CHECKSUM 72d820dec546752e5a8303b33b009079c15c2390ce76d67cf514991646c6127b
ENV GOPATH /go
ENV PATH $PATH:$GOPATH/bin:/usr/local/go/bin
RUN curl -fsSL "$GOLANG_DOWNLOAD_URL" -o golang.tar.gz && \
    echo "$GOLANG_SHA256_CHECKSUM golang.tar.gz" | sha256sum -c - && \
    sudo tar -C /usr/local -xzf golang.tar.gz && \
    rm golang.tar.gz && \
    mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
#End: install golang

RUN go get -u -d gocv.io/x/gocv
WORKDIR $GOPATH/src/gocv.io/x/gocv
RUN make install

RUN rm -rf /opencv-$OPENCV_VERSION /opencv_contrib-$OPENCV_VERSION
RUN ls /
