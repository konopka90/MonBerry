"""
This module reads data from BME280 and push samples to InfluxDB database.
"""
import os
import random
from datetime import datetime
from time import sleep

import bme280
import smbus2
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

sim = False
temperature = 0.0
humidity = -1
pressure = -1

TOKEN = "cJ6YQc3-8I43zA6V6tns5adjjCV0-176kWEoRhIolxVdjArSpYYrUaZ0Bv7_oJSP4tQhaG7RyiOb-ZJ2rG0iqw=="
ORG = "pi"
BUCKET = "pi"

url = os.environ.get('INFLUXDB_URL', 'http://localhost:8086')
interval = int(os.environ.get('POLLING_INTERVAL', 5))
sim = os.environ.get('SIMULATION_MODE', 'no') == 'yes'
device_port = int(os.environ.get('DEVICE_PORT', 1))
device_address = int(os.environ.get('DEVICE_ADDRESS', '0x76'), 0)
is_ok_counter = 0

print('* Configuration *')
print(f'INFLUXDB_URL={url}')
print(f'SIMULATION_MODE={sim}')
print(f'POLLING_INTERVAL={interval}')
print(f'DEVICE_PORT={device_port}')
print(f'DEVICE_ADDRESS={device_address}')

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

            data = bme280.sample(bus, device_address, calibration_params)
            
            temperature = data.temperature
            pressure = data.pressure
            humidity = data.humidity

        with InfluxDBClient(url=url, token=TOKEN) as client:
            with client.write_api(write_options=SYNCHRONOUS) as write_api:
                point = Point("mem")\
                    .tag("host", "pi")\
                    .field("temperature", temperature)\
                    .field("pressure", pressure)\
                    .field("humidity", humidity)\
                    .time(datetime.utcnow(), WritePrecision.NS)

                write_api.write(BUCKET, ORG, point)

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

