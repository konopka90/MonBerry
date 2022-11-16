from pydoc import tempfilepager
import random

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

temperature = 20 + random.random() * 10
pressure = 1000.0 + random.random() * 10.0
humidity = random.random() * 100.0

# You can generate a Token from the "Tokens Tab" in the UI
token = "cJ6YQc3-8I43zA6V6tns5adjjCV0-176kWEoRhIolxVdjArSpYYrUaZ0Bv7_oJSP4tQhaG7RyiOb-ZJ2rG0iqw=="
org = "pi"
bucket = "pi"
client = InfluxDBClient(url="http://localhost:8086", token=token)

def insertData(t, p, h):
    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = Point("mem")\
        .tag("host", "pi")\
        .field("temperature", t)\
        .field("pressure", p)\
        .field("humidity", h)\
        .time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, point)


insertData(temperature, pressure, humidity)



