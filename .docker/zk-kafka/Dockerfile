# syntax = docker/dockerfile:1.2
FROM ubuntu:22.04
LABEL maintainer="Matthew McCann <matmccann@gmail.com>"
USER root

ENV DEBIAN_FRONTEND noninteractive
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-amd64
EXPOSE 22 2181 2888 3888 9200

RUN export PATH=$JAVA_HOME/bin:$PATH
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# Download, install, and set up zk-kafka
COPY apt /start/apt
COPY configs /start/configs
COPY scripts /start/scripts
RUN chmod 775 /start -R
# install apt packages
RUN --mount=type=cache,target=/var/cache/apt apt-get update -yqq && \
    apt-get install -yqq --no-install-recommends \
    $(cat /start/apt/general.apt) \
    $(cat /start/apt/kafka.apt) \
    $(cat /start/apt/supervisord.apt) && \
     rm -rf /var/lib/apt/lists/*

# Install kafka and copy configs
RUN /start/scripts/install_kafka.sh
COPY configs/kafka-server.properties /opt/kafka/config/server.properties

# Setup supervisord to run kafka and zookeeper processes
COPY configs/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor

# Set up docker for runtime
RUN rm -rf /start
HEALTHCHECK CMD echo stat | nc 127.0.0.1 2181
WORKDIR "/opt/kafka"
CMD ["/usr/bin/supervisord"]