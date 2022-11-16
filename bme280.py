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
username = "pi"
password = "SecurePassword2137"
with InfluxDBClient(url="http://localhost:8086", token=f'{username}:{password}') as client:
    with client.write_api(write_options=SYNCHRONOUS) as write_api:
        point = Point("mem")\
            .tag("host", "pi")\
            .field("temperature", temperature)\
            .field("pressure", pressure)\
            .field("humidity", humidity)\
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point)



