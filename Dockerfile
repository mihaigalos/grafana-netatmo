ARG ARCH=

# Pull base image
FROM ubuntu:latest

# Setup external package-sources
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-virtualenv \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# RUN pip install setuptools
RUN pip3 install --break-system-packages pytz influxdb-client requests lnetatmo

# Environment vars
ENV PYTHONIOENCODING=utf-8

# Copy files
ADD netatmo_influx.py /

ADD get.sh /

# Run
CMD ["/bin/bash","/get.sh"]
