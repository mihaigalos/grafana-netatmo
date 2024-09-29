#!/usr/bin/env python3
# encoding=utf-8

import lnetatmo, os
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime

authorization = lnetatmo.ClientAuth()

weatherData = lnetatmo.WeatherStationData(authorization)

influxdb2_org=os.getenv('INFLUXDB2_ORG', "Home")
influxdb2_token=os.getenv('INFLUXDB2_TOKEN', "token")
client = InfluxDBClient(url="http://192.168.1.86:8086", token=influxdb2_token, org=influxdb2_org, verify_ssl=False)
# if {'name': 'netatmo'} not in client.get_list_database():
#     client.create_database('netatmo')

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


bucket="Staging"

for station in weatherData.stations:
    station_data = []
    module_data = []
    station = weatherData.stationById(station)
    station_name = station['station_name']
    altitude = station['place']['altitude']
    country= station['place']['country']
    timezone = station['place']['timezone']
    longitude = station['place']['location'][0]
    latitude = station['place']['location'][1]
    for module, moduleData in weatherData.lastData(station=station_name, exclude=3600).items():
        for measurement in ['altitude', 'country', 'longitude', 'latitude', 'timezone']:
            value = eval(measurement)
            if type(value) == int:
                value = float(value)
            timestamp = datetime.datetime.fromtimestamp(moduleData['When']).strftime("%Y-%m-%dT%H:%M:%SZ")
            station_data.append({
                "measurement": measurement,
                "tags": {
                    "station": station_name,
                    "module": module
                },
                "time": timestamp,
                "fields": {
                    "value": value
                }
            })

        for sensor, value in moduleData.items():
            if sensor.lower() != 'when':
                if type(value) == int:
                    value = float(value)
                timestamp = datetime.datetime.fromtimestamp(moduleData['When']).strftime("%Y-%m-%dT%H:%M:%SZ")
                module_data.append({
                    "measurement": sensor.lower(),
                    "tags": {
                        "station": station_name,
                        "module": module,
                        "source": "docker netatmo-influx",
                        "origin": "Netatmo"
                    },
                    "time": timestamp,
                    "fields": {
                        "value": value
                    }
                })

    print("\n\n----------------------------------- Station data -----------------------------------")
    print(station_data)
    print("\n\n----------------------------------- Module data -----------------------------------")
    print(*module_data, sep="\n")


    write_api.write(bucket=bucket, record=station_data, time_precision='s')
    write_api.write(bucket=bucket, record=module_data, time_precision='s')

    # client.write_points(station_data, time_precision='s', database='netatmo')
    # client.write_points(module_data, time_precision='s', database='netatmo')
