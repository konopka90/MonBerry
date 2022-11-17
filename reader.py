from sys import argv
import os
from time import sleep
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
interval = int(os.environ.get('POLLING_INTERVAL', 5))
sim = os.environ.get('SIMULATION_MODE', 'no') == 'yes'
device_port = int(os.environ.get('DEVICE_PORT', 1))
device_address = int(os.environ.get('DEVICE_ADDRESS', '0x76'), 0)
is_ok_counter = 0

print('* Configuration *')
print('INFLUXDB_URL={}'.format(url))
print('SIMULATION_MODE={}'.format(sim))
print('POLLING_INTERVAL={}'.format(interval))
print('DEVICE_PORT={}'.format(device_port))
print('DEVICE_ADDRESS={}'.format(device_address))

while True:
    try:
        if sim:
            temperature = 20 + random.random() * 10
            pressure = 1000.0 + random.random() * 10.0
            humidity = random.random() * 100.0
        else:
            # BME280 setup
            bus = smbus2.SMBus(device_port)
            calibration_params = bme280.load_calibration_params(
                bus, device_address)

            # the sample method will take a single reading and return a
            # compensated_reading object
            data = bme280.sample(bus, device_address, calibration_params)

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

        is_ok_counter = is_ok_counter + 1
        if is_ok_counter == 1:
            print("Working...")

    except OSError as dev_exception:
        is_ok_counter = 0
        print("Cannot read from device: " +
              dev_exception.strerror + ", code: " + str(dev_exception.errno))
    except Exception as e:
        is_ok_counter = 0
        print("Unknown exception: " + str(e))

    sleep(interval)
