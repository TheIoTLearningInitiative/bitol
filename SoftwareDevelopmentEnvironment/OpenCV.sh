#!/bin/sh

set -x

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

sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove

sudo apt-get -y install build-essential

sudo apt-get -y install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

sudo apt-get -y install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install libgtk-3-dev
sudo apt-get -y install libatlas-base-dev gfortran
sudo apt-get -y install python2.7-dev python3.5-dev

sudo apt-get -y install python-pip && pip install --upgrade pip
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

cat << EOM >> $HOME/.bashrc

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

EOM

sleep 1

. $HOME/.bashrc

mkvirtualenv cv -p python3
workon cv
pip install numpy

cd $HOME

git clone https://github.com/opencv/opencv/
git clone https://github.com/opencv/opencv_contrib
cd ~/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
      -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
      -D BUILD_EXAMPLES=ON ..

make -j4
sudo make install
sudo ldconfig
cd /usr/local/lib/python3.5/site-packages/
ls -l
sudo mv cv2.cpython-35m-x86_64-linux-gnu.so cv2.so
cd ~/.virtualenvs/cv/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so

cd $ROOT_DIRECTORY

pip install imutils

# End of File
