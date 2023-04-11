# Home Surveillance System

## Description
This project is provides a basic home surveillance system that connects to IP cameras on a fixed local network.
The videos from IP cameras are sent to a media server where they are recorded (HLS) and periodically backed up (local or cloud).
You may view the cameras by logging in to Ant Media Server (the video server) to check out what things look like at home.

To monitor the health of the system (device monitoring), a visualization stack with Kafka messaging fabric has been installed.
The device monitoring system may also be viewed with a GUI to show any interruption to the camera streams, downed devices, and so more.

## TL-DR

```bash
# spin up the project containers
docker compose up --build -d
# configure the grafana dashboard
cd .docker/grafana; ./grafana-setup.sh
```

## Sending video to the Media Server


__testing__

- from the `gstreamer` docker container you can send a stream to the server

```bash
docker exec -it gstreamer bash
  # test stream 
  gst-launch-1.0 -v videotestsrc ! x264enc ! flvmux ! rtmpsink location='rtmp://172.23.0.2/WebRTCApp/test-101 live=1'
```

__set up an IP camera__

- navigate to ant media server url: http://172.23.0.2:5080
- on the left, select WebRTCApp
- click 'New Live Stream'
- select IP Camera and fill in the details for your camera so that Ant Media Server can connect with it and start pulling its streams


## Configuring video backups

- you can add an S3 account and update `S3_ACCOUNT` in `src/.env` so that it will push to your S3 bucket
- otherwise, it will store them locally in a folder (`streams`) in the root directory of this project

## Viewing video streams

- login to the Ant Media Server dashboard: http://172.23.0.2:5080
- create a username and password
- navigate to WebRTCApp


## Device Monitoring

- login to the grafana dashboard: http://172.23.0.10:3000
- create a new username and password
- navigate to dashboard, and select antmediaserver

