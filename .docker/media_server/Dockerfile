# syntax = docker/dockerfile:1.2
FROM ubuntu:20.04
LABEL maintainer="Matthew McCann <matmccann@gmail.com>"
ENV AntMediaServer="https://github.com/ant-media/Ant-Media-Server/releases/download/ams-v2.5.3/ant-media-server-community-2.5.3.zip"
ENV AMS_DL="ant-media-server-community-2.5.3.zip"
ARG KAFKA_BROKER
ARG MongoDBServer
ARG MongoDBUsername
ARG MongoDBPassword
ENV MongoDBConn="mongodb://${MongoDBUsername}:${MongoDBPassword}@${MongoDBServer}:27017"


ARG BranchName=master

#Running update and install makes the builder not to use cache which resolves some updates
RUN --mount=type=cache,target=/var/cache/apt apt-get update -yqq  \
    && apt-get install -yqq curl libcap2 wget net-tools iproute2 cron logrotate unzip iptables

RUN cd /home && wget $AntMediaServer

# install AMS from zip file
RUN cd home \
    && pwd \
    && wget https://raw.githubusercontent.com/ant-media/Scripts/${BranchName}/install_ant-media-server.sh \
    && chmod 755 install_ant-media-server.sh \
    && ./install_ant-media-server.sh -i ${AMS_DL} -s false

# Override default AMS settings
RUN sed -i "s/^server.kafka_brokers=.*/server.kafka_brokers=${KAFKA_BROKER}/g" /usr/local/antmedia/conf/red5.properties
RUN sed -i "s/^clusterdb.host=.*/clusterdb.host=${MongoDBServer}:27017/g" /usr/local/antmedia/conf/red5.properties
RUN sed -i "s/^clusterdb.user=.*/clusterdb.user=${MongoDBUsername}/g" /usr/local/antmedia/conf/red5.properties
RUN sed -i "s/^clusterdb.password=.*/clusterdb.password=${MongoDBPassword}/g" /usr/local/antmedia/conf/red5.properties

#RUN bash -c "/usr/local/antmedia/change_server_mode.sh cluster '${MongoDBServer}:27017' '${MongoDBUsername}' '${MongoDBPassword}' ";

## Options
## -g: Use global(Public) IP in network communication. Its value can be true or false. Default value is false.
##
## -s: Use Public IP as server name. Its value can be true or false. Default value is false.
##
## -r: Replace candidate address with server name. Its value can be true or false. Default value is false
##
## -m: Server mode. It can be standalone or cluster. If cluster mode is specified then mongodb host, username and password should also be provided.
##     There is no default value for mode
##
## -h: MongoDB or Redist host. It's either IP address or full connection string such as mongodb://[username:password@]host1[:port1] or mongodb+srv://[username:password@]host1[:port1] or redis://[username:password@]host1[:port1] or redis yaml configuration
##
## -u: MongoDB username: Deprecated. Just give the username in the connection string with -h parameter
##
## -p: MongoDB password: Deprecated. Just give the password in the connection string with -h parameter
##
## -l: Licence Key
#
## -a: TURN/STUN Server URL for the server side. It should start with "turn:" or "stun:" such as stun:stun.l.google.com:19302 or turn:ovh36.antmedia.io
##     this url is not visible to frontend users just for server side.
##
## -n: TURN Server Usermame: Provide the TURN server username to get relay candidates.
##
## -w: TURN Server Password: Provide the TURN server password to get relay candidates.
#
ENTRYPOINT ["/usr/local/antmedia/start.sh", "-h", "${MongoDBConn}"]
