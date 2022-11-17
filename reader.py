from sys import argv
import os
import smbus2
import bme280
import random
import sys
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

sim = False
temperature = 0.0
humidity = -1
pressure = -1

# You can generate a Token from the "Tokens Tab" in the UI
token = "cJ6YQc3-8I43zA6V6tns5adjjCV0-176kWEoRhIolxVdjArSpYYrUaZ0Bv7_oJSP4tQhaG7RyiOb-ZJ2rG0iqw=="
org = "pi"
bucket = "pi"
url = os.environ.get('INFLUXDB_URL', 'http://localhost:8086')

if len(sys.argv) > 1 and sys.argv[1] == "--sim":
    sim = True

if sim:
    temperature = 20 + random.random() * 10
    pressure = 1000.0 + random.random() * 10.0
    humidity = random.random() * 100.0
else:
    # BME280 setup
    port = 0
    address = 0x76
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)

    # the sample method will take a single reading and return a
    # compensated_reading object
    data = bme280.sample(bus, address, calibration_params)

    temperature = data.temperature
    pressure = data.pressure
    humidity = data.humidity

with InfluxDBClient(url=url, token=token) as client:
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        point = Point("mem")\
            .tag("host", "pi")\
            .field("temperature", temperature)\
            .field("pressure", pressure)\
            .field("humidity", humidity)\
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point)
