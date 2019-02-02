# Mjpeg-Streamer

## Build

```sh
$ docker build -t xe1gyq/mjpeg-streamer .
```

## Run

```sh
$ docker run -it --device /dev/video0 xe1gyq/mjpeg-streamer 8080
```
