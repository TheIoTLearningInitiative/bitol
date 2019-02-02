# Mjpeg-Streamer

## Setup

```
pi@raspberrypi:~ $ sudo apt-get install cmake libjpeg8-dev
pi@raspberrypi:~ $ sudo apt-get install gcc g++ cmake
```

```sh
pi@raspberrypi:~ $ git clone https://github.com/jacksonliam/mjpg-streamer.git
Cloning into 'mjpg-streamer'...
remote: Enumerating objects: 2885, done.
remote: Total 2885 (delta 0), reused 0 (delta 0), pack-reused 2885
Receiving objects: 100% (2885/2885), 3.49 MiB | 345.00 KiB/s, done.
Resolving deltas: 100% (1825/1825), done.
```

```sh
pi@raspberrypi:~ $ cd mjpg-streamer/
pi@raspberrypi:~/mjpg-streamer $ ls
README.md  mjpg-streamer-experimental
pi@raspberrypi:~/mjpg-streamer $ cd mjpg-streamer-experimental/
pi@raspberrypi:~/mjpg-streamer/mjpg-streamer-experimental $ ls
CMakeLists.txt  TODO             mjpg_streamer.h         start.sh
Dockerfile      cmake            mjpg_streamer@.service  utils.c
LICENSE         docker-start.sh  plugins                 utils.h
Makefile        makedeb.sh       postinstall.sh          www
README.md       mjpg_streamer.c  scripts
```

```sh
pi@raspberrypi:~/mjpg-streamer/mjpg-streamer-experimental $ make
[ -d _build ] || mkdir _build
[ -f _build/Makefile ] || (cd _build && cmake  -DCMAKE_BUILD_TYPE=Release ..)
-- The C compiler identification is GNU 6.3.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
...
...
```

```sh
pi@raspberrypi:~/mjpg-streamer/mjpg-streamer-experimental $ export LD_LIBRARY_PATH=.
```

```sh
pi@raspberrypi:~/mjpg-streamer/mjpg-streamer-experimental $ ./mjpg_streamer -o "output_http.so -w ./www" -i "input_uvc.so"
MJPG Streamer Version: git rev: ddb69b7b4f114f3c2ca01adf55712792ca8aed43
 i: Using V4L2 device.: /dev/video0
 i: Desired Resolution: 640 x 480
 i: Frames Per Second.: -1
 i: Format............: JPEG
 i: TV-Norm...........: DEFAULT
UVCIOC_CTRL_ADD - Error at Pan (relative): Inappropriate ioctl for device (25)
UVCIOC_CTRL_ADD - Error at Tilt (relative): Inappropriate ioctl for device (25)
UVCIOC_CTRL_ADD - Error at Pan Reset: Inappropriate ioctl for device (25)
UVCIOC_CTRL_ADD - Error at Tilt Reset: Inappropriate ioctl for device (25)
UVCIOC_CTRL_ADD - Error at Pan/tilt Reset: Inappropriate ioctl for device (25)
UVCIOC_CTRL_ADD - Error at Focus (absolute): Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Pan (relative): Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Tilt (relative): Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Pan Reset: Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Tilt Reset: Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Pan/tilt Reset: Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Focus (absolute): Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at LED1 Mode: Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at LED1 Frequency: Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Disable video processing: Inappropriate ioctl for device (25)
UVCIOC_CTRL_MAP - Error at Raw bits per pixel: Inappropriate ioctl for device (25)
 o: www-folder-path......: ./www/
 o: HTTP TCP port........: 8080
 o: HTTP Listen Address..: (null)
 o: username:password....: disabled
 o: commands.............: enabled
```
