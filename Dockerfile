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

RUN useradd -m -u 1001 -s /bin/bash user
USER user
WORKDIR /home/user

RUN pip3 install --break-system-packages pytz influxdb-client requests lnetatmo

ENV PYTHONIOENCODING=utf-8
ADD netatmo_influx.py .
ADD get.sh .

CMD ["/bin/bash","get.sh"]
