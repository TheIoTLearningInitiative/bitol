apk update
apk add --no-cache git libtool automake autoconf expat-dev gcc make cmake g++ python py-lxml py-pip ccache gawk freetype-dev libpng-dev python-dev gfortran ca-certificates openssl linux-headers

pip install pip --upgrade 
pip install pyserial scipy future 

git clone git://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive;
cd

ln -s /usr/include/locale.h /usr/include/xlocale.h
sed -i 's/, int,/, unsigned int,/' /usr/include/assert.h

pip install pymavlink MAVProxy

echo 'export PATH=$PATH:/ardupilot/Tools/autotest' >> /etc/profile
echo 'export PATH=/usr/lib/ccache:$PATH' >> /etc/profile
echo 'export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH' >> /etc/profile

cd ardupilot/ArduPlane
sed -i 's/feenableexcept(exceptions);/\/\/feenableexcept(exceptions);/' /ardupilot/libraries/AP_HAL_SITL/Scheduler.cpp
sed -i 's/int old = fedisableexcept(FE_OVERFLOW);/int old = 1;/' /ardupilot/libraries/AP_Math/matrix_alg.cpp
sed -i 's/if (old >= 0 && feenableexcept(old) < 0)/if (0)/' /ardupilot/libraries/AP_Math/matrix_alg.cpp
sed -i "s/#include <sys\/types.h>/#include <sys\/types.h>\n\n#define TCGETS2 _IOR('T', 0x2A, struct termios2)\n#define TCSETS2 _IOW('T', 0x2B, struct termios2)/" /ardupilot/libraries/AP_HAL_SITL/UART_utils.cpp
. /etc/profile && sim_vehicle.py -w
cd
cd ardupilot/
rm -rf .git/objects/pack 

apk del 
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
