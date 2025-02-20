from fastapi import FastAPI, HTTPException
from app.core.config import get_settings
from app.models.sensor import SensorDataBase, SensorDataResponse
from app.services.kafka_service import KafkaService
from app.services.postgres_service import PostgresService
from app.utils.metrics import setup_metrics
from app.core.logging import setup_logging
from contextlib import asynccontextmanager
from kafka import KafkaConsumer
import asyncio
import pandas as pd
import json
from datetime import datetime

# Setup logging
logger = setup_logging()

# Get settings
settings = get_settings()

# Initialize services
kafka_service = KafkaService()
postgres_service = PostgresService()

async def consume_data():
    while True:
        try:
            consumer = KafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id=settings.KAFKA_CONSUMER_GROUP,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                api_version=(2, 5, 0)
            )
            for message in consumer:
                await postgres_service.store_sensor_data(message.value)
        except Exception as e:
            logger.error(f"Error in consumer: {str(e)}")
            await asyncio.sleep(5)

def transform_sensor_data(data: SensorDataBase) -> SensorDataResponse:
    data_dict = {
        "device_id": data.device_id,
        "temperature": data.temperature,
        "pressure": data.pressure,
        "timestamp": data.timestamp.isoformat(),
    }
    df = pd.DataFrame([data_dict])
    df['temperature_f'] = df['temperature'] * 9/5 + 32
    df['pressure_psi'] = df['pressure'] * 0.145038
    transformed = df.to_dict(orient='records')[0]
    return SensorDataResponse(**transformed)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

@app.post("/api/v1/sensor/ingest", response_model=SensorDataResponse)
async def ingest_sensor_data(data: SensorDataBase):
    try:
        transformed_data = transform_sensor_data(data)
        # Convert datetime to string before sending to Kafka
        kafka_data = transformed_data.dict()
        kafka_data['timestamp'] = kafka_data['timestamp'].isoformat()
        await kafka_service.send_message(settings.KAFKA_TOPIC, kafka_data)
        return transformed_data
    except Exception as e:
        logger.error(f"Error processing sensor data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") 