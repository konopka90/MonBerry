# raspberry-enviro

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
