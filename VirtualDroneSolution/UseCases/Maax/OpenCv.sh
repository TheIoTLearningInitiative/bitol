#!/bin/sh

OPENCV_VERSION=3.4.2
apk add --update --no-cache build-base clang clang-dev cmake pkgconf wget
apk add --update --no-cache linux-headers libjpeg-turbo libjpeg-turbo-dev libpng libpng-dev
apk add --update --no-cache libwebp libwebp-dev tiff tiff-dev jasper-libs jasper-dev
apk add --update --no-cache libavc1394 libavc1394-dev
apk add --update --no-cache gstreamer gstreamer-dev gst-plugins-base gst-plugins-base-dev libgphoto2 libgphoto2-dev 

#apk add --update --no-cache openblas openblas-dev
#apk add --update --no-cache openexr openexr-dev ffmpeg-libs ffmpeg-dev

apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --update --no-cache libtbb libtbb-dev

# Python dependencies
apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --update --no-cache python3 python3-dev
apk add --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
        --update --no-cache py-numpy py-numpy-dev openblas openblas-dev openexr openexr-dev ffmpeg-libs ffmpeg-dev

#apk add --update --no-cache openblas openblas-dev                                                                                                                                       
#apk add --update --no-cache openexr openexr-dev ffmpeg-libs ffmpeg-dev                                                                                                                  

# Make Python3 as default
ln -vfs /usr/bin/python3 /usr/local/bin/python
ln -vfs /usr/bin/pip3 /usr/local/bin/pip

# Fix libpng path
ln -vfs /usr/include/libpng16 /usr/include/libpng
ln -vfs /usr/include/locale.h /usr/include/xlocale.h

# Download OpenCV source
cd /tmp
wget https://github.com/opencv/opencv/archive/$OPENCV_VERSION.tar.gz
tar -xvzf $OPENCV_VERSION.tar.gz
#rm -vrf $OPENCV_VERSION.tar.gz

# Configure
mkdir -vp /tmp/opencv-$OPENCV_VERSION/build
cd /tmp/opencv-$OPENCV_VERSION/build

cmake \
    # Compiler params
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_C_COMPILER=/usr/bin/clang \
    -D CMAKE_CXX_COMPILER=/usr/bin/clang++ \
    -D CMAKE_INSTALL_PREFIX=/usr \
    -D INSTALL_PYTHON_EXAMPLES=NO \
    -D INSTALL_C_EXAMPLES=NO \
    -D WITH_IPP=NO \
    -D WITH_1394=NO \
    -D WITH_LIBV4L=NO \
    -D WITH_V4l=YES \
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
    -D BUILD_ANDROID_EXAMPLES=NO \
    -D PYTHON3_LIBRARY=`find /usr -name libpython3.so` \
    -D PYTHON_EXECUTABLE=`which python3` \
    -D PYTHON3_EXECUTABLE=`which python3` \
    -D BUILD_opencv_python3=YES ..

exit 0

# Build
make -j`grep -c '^processor' /proc/cpuinfo`
make install

# Cleanup
cd /
rm -vrf /tmp/opencv-$OPENCV_VERSION
apk del --purge build-base clang clang-dev cmake pkgconf wget openblas-dev \
        openexr-dev gstreamer-dev gst-plugins-base-dev libgphoto2-dev \
        libtbb-dev libjpeg-turbo-dev libpng-dev tiff-dev jasper-dev \
        ffmpeg-dev libavc1394-dev python3-dev py-numpy-dev
rm -vrf /var/cache/apk/*
