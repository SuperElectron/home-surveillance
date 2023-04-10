# syntax = docker/dockerfile:1.2
FROM ubuntu:20.04
LABEL maintainer="Matthew McCann <matmccann@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN echo "DEBIAN_FRONTEND: $DEBIAN_FRONTEND"

COPY start /start
RUN chmod 775 /start -R && ls -al /start
RUN /start/setup.sh
RUN /start/install_gst.sh

HEALTHCHECK CMD ping -c3 -i 10 127.0.0.1

CMD "bash"
