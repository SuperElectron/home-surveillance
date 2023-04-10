#!/bin/bash

# Example usage: ./setup.sh

export WORKDIR="/start"
export NAME="[install.sh]: "
echo "${NAME} STARTING "

# Bash failure reporting for the script
set -eE -o functrace
failure() {
  local lineno=$1
  local msg=$2
  echo "${NAME} Failed at $lineno: $msg"
}
trap '${NAME} failure ${LINENO} "$BASH_COMMAND"' ERR

echo "${NAME} Installing kafka to /opt/kafka "
cd /tmp && \
  curl -OL https://archive.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz && \
  tar -zxvf kafka_2.12-2.2.0.tgz && \
  mv kafka_2.12-2.2.0 kafka && \
  mv kafka /opt/

echo "${NAME} Copy kafka server properties "
mkdir -p /tmp/kafka-logs
chmod 777 /tmp/kafka-logs

echo "${NAME} FINISHED "
