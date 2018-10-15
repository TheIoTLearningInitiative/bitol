#!/bin/bash

# =============================================================================
# Variables
# =============================================================================

# None

# =============================================================================
# Functions
# =============================================================================

# None

# =============================================================================
# Main
# =============================================================================

apk update
apk add --no-cache git libtool automake autoconf expat-dev gcc make cmake g++ python py-lxml py-pip ccache gawk freetype-dev libpng-dev python-dev gfortran ca-certificates openssl linux-headers

ln -s /usr/include/locale.h /usr/include/xlocale.h
sed -i 's/, int,/, unsigned int,/' /usr/include/assert.h

pip install pip --upgrade
pip install sphinx monotonic future nose mock sphinx-3dr-theme
pip install pymavlink
pip install dronekit
pip install dronekit-sitl -UI
pip install paho-mqtt
pip install ppretty

git clone https://github.com/dronekit/dronekit-python.git
cd dronekit-python
python setup.py build
python setup.py install

apk del build-base cmake automake autoconf ccache openssl ca-certificates gawk
rm -rf /var/cache/apk/*
rm -rf /root/.ccache
rm -rf /root/.config
rm -rf /root/.ash_history
rm -rf /root/.tilecache

# End of File
