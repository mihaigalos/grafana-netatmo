
@_default:
  just --list --unsorted

_setup:
  #!/bin/bash
  [ -d .env ] && exit 0 || python3 -m venv .env && . .env/bin/activate && pip install -r requirements.txt


run_influx:
  docker run -p 8086:8086 \
    -v "$PWD/data:/var/lib/influxdb2" \
    -v "$PWD/config:/etc/influxdb2" \
    -v "$PWD/scripts:/docker-entrypoint-initdb.d" \
    -e DOCKER_INFLUXDB_INIT_MODE=setup \
    -e DOCKER_INFLUXDB_INIT_USERNAME=user \
    -e DOCKER_INFLUXDB_INIT_PASSWORD=password \
    -e DOCKER_INFLUXDB_INIT_ORG=Home \
    -e DOCKER_INFLUXDB_INIT_BUCKET=Staging \
    -e V1_DB_NAME=mydb \
    -e V1_RP_NAME=myrp \
    -e V1_AUTH_USERNAME=user \
    -e V1_AUTH_PASSWORD=password \
    influxdb:2

run: _setup
  . .env/bin/activate && ./get.sh
