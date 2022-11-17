# MonBerry
The MonBerry is a docker-compose stack to monitor temperature, humidity and pressure using RaspberryPi and BME280 sensor via i2c interface.
It supports also simulation mode where BME280 sensor is stubbed with random values.

## Overview
The MonBerry brings up several docker containers:
- Grafana to aggregate and visualize data
- InfluxDB to store time series data
- Reader to collect measurements from BME280 and push to InfluxDB database

## Hardware requirements
- RaspberryPi 3 (should also work with different versions)
- BME280 sensor

## Sofware requirements
The MonBerry is tested with Raspbian GNU/Linux 11 (bullseye). 

Recommended software:
- Docker 20.10.21
- Docker compose v2.12.2
- Python 3.9.2

## Enable i2c interface

To handle BME280 sensor you need to enable i2c support on RaspberryPi.

[Check here](https://www.mathworks.com/help/supportpkg/raspberrypiio/ref/enablei2c.html)

## How to build

```bash
docker compose build
```

## How to run

```bash
docker compose up -d
```

or use simulation mode

```bash
SIMULATION_MODE=yes docker compose up -d
```

## How to kill

```bash
docker compose down
```

## How to kill and remove data

```bash
docker compose down --volumes
```

## How to show visualization

1. Go to Grafana dashboards [open dashboards](http://localhost:3000/dashboards) 
2. Open "Temperature - Pressure - Humidity" dashboard.

## Development

Create and activate env

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```
