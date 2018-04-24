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

pip install pip --upgrade
pip install sphinx monotonic future nose mock sphinx-3dr-theme
pip install pymavlink
pip install dronekit
pip install dronekit-sitl -UI

git clone https://github.com/dronekit/dronekit-python.git
cd dronekit-python
python setup.py build
python setup.py install

# End of File
