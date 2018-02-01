FROM ubuntu:xenial

MAINTAINER Steven Spinner <stevenmspin1003@gmail.com>

# Install the needed packages for a Groundr instance
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y install sudo \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y install curl \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y install wget \
	&& DEBIAN_FRONTEND=noninteractove apt-get -y install git \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y install python3 \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip \
	&& DEBIAN_FRONTEND=noninteractive apt-get -y autoremove --purge \
	&& apt-get -y clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -f /var/cache/apt/*.bin \
	&& pip3 install flask \
	&& cd /root \
	&& wget https://raw.githubusercontent.com/uf-mil/Groundr/master/demo/scripts/start.sh \
	&& chmod +x start.sh
