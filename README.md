1. Open project

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

4. Start the infrastructure services:

```bash
docker compose up -d
```

5. Start the FastAPI server:

```bash
python main.py
```

## Project Structure

```
joby_interface/
├── app/
│   ├── core/
│   │   ├── config.py      # Application configuration
│   │   └── logging.py     # JSON logging setup
│   ├── models/
│   │   └── sensor.py      # Pydantic models for data validation
│   ├── services/
│   │   ├── kafka_service.py   # Kafka producer/consumer
│   │   └── postgres_service.py # Database operations
│   └── utils/
│       └── metrics.py     # Prometheus metrics
├── main.py               # FastAPI application
├── test_api.py          # API tests
├── init.sql             # Database initialization
├── docker-compose.yml   # Infrastructure setup
└── requirements.txt     # Python dependencies
```

## API Documentation

### POST /api/v1/sensor/ingest

Ingests sensor data and performs unit conversion.

Example Request (from models/sensor.py):

```python:joby_interface/app/models/sensor.py
startLine: 19
endLine: 26
```

Response includes the original data plus converted units:

- Temperature in Fahrenheit (°F)
- Pressure in PSI

## Key Components

### Data Flow

1. FastAPI endpoint receives sensor data:

```
python:joby_interface/main.py
startLine: 61
endLine: 72
```

2. Data transformation and unit conversion:

```
python:joby_interface/main.py
startLine: 43
endLine: 54
```

3. Kafka message publishing with circuit breaker:

```
python:joby_interface/app/services/kafka_service.py
startLine: 25
endLine: 36
```

4. PostgreSQL storage:

```
python:joby_interface/app/services/postgres_service.py
startLine: 26
endLine: 45
```

### Infrastructure

Docker Compose provides:

```
yaml:joby_interface/docker-compose.yml
startLine: 1
endLine: 26
```

## Testing

Run the test suite:

```bash
python test_api.py
```

Test implementation:

```
python:joby_interface/test_api.py
startLine: 5
endLine: 27
```

## Environment Variables

Configuration settings (defaults shown):

```
python:joby_interface/app/core/config.py
startLine: 6
endLine: 28
```

## Monitoring

### Metrics

Prometheus metrics:

```
python:joby_interface/app/utils/metrics.py
startLine: 6
endLine: 8
```

### Logging

JSON-structured logging:

```
python:joby_interface/app/core/logging.py
startLine: 5
endLine: 14
```

## Database Schema

PostgreSQL table structure:

```
sql:joby_interface/init.sql
startLine: 1
endLine: 7
```
