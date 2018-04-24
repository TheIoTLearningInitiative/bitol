apk update && apk add --no-cache\
	git \
	libtool \ 
	automake \
	autoconf \
	expat-dev \
	gcc \
	make \
	cmake \
	g++ \
	python \
	py-lxml \
	py-pip \
	ccache \
	gawk \
	freetype-dev \
	libpng-dev \
	python-dev \
	gfortran \
	ca-certificates \
	openssl \
	linux-headers

#pip install pip matplotlib \
#	pyserial \
#	scipy \
#	pexpect \
#	future 

#update-ca-certificates && \
#	cd /tmp && \
#	wget -O opencv-2.4.13.4.tar.gz https://github.com/opencv/opencv/archive/2.4.13.4.tar.gz && \
#	tar -xzf opencv-2.4.13.4.tar.gz &&\
#	cd /tmp/opencv-2.4.13.4 && \
#	mkdir build && \
#	cd build && \
#	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_FFMPEG=NO -D WITH_IPP=NO -D WITH_OPENEXR=NO .. && \
#	make VERBOSE=1 && \
#	make && \
#	make install 

cd
git clone git://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive;

cd
git clone git://github.com/tridge/jsbsim.git
cd jsbsim 
./autogen.sh --enable-libraries && make
rm -rf .git

ln -s /usr/include/locale.h /usr/include/xlocale.h
sed -i 's/, int,/, unsigned int,/' /usr/include/assert.h

pip install pymavlink \
	MAVProxy

echo 'export PATH=$PATH:/jsbsim/src' >> /etc/profile && \
	echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> /etc/profile && \
	echo 'export PATH=/usr/lib/ccache:$PATH' >> /etc/profile && \
	echo 'export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH' >> /etc/profile

cd
cd ardupilot/ArduPlane
sed -i 's/feenableexcept(exceptions);/\/\/feenableexcept(exceptions);/' /ardupilot/libraries/AP_HAL_SITL/Scheduler.cpp  && \
	sed -i 's/int old = fedisableexcept(FE_OVERFLOW);/int old = 1;/' /ardupilot/libraries/AP_Math/matrix_alg.cpp && \
	sed -i 's/if (old >= 0 && feenableexcept(old) < 0)/if (0)/' /ardupilot/libraries/AP_Math/matrix_alg.cpp && \
	sed -i "s/#include <sys\/types.h>/#include <sys\/types.h>\n\n#define TCGETS2 _IOR('T', 0x2A, struct termios2)\n#define TCSETS2 _IOW('T', 0x2B, struct termios2)/" /ardupilot/libraries/AP_HAL_SITL/UART_utils.cpp
. /etc/profile && sim_vehicle.py -w
cd
cd ardupilot/
rm -rf .git/objects/pack 

apk del \
	build-base \
	cmake \
	automake \
	autoconf \
	ccache \
	openssl \
	ca-certificates \
	gawk && \
	rm -rf /var/cache/apk/* && \
	rm -rf /tmp/opencv* && \
	rm -rf /root/.ccache && \
	rm -rf /root/.config && \
	rm -rf /root/.ash_history && \
	rm -rf /root/.tilecache && \
