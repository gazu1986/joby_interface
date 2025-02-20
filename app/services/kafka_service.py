from typing import Dict, Any
from kafka import KafkaProducer, KafkaConsumer
from app.core.config import get_settings
from app.utils.metrics import PROCESSED_MESSAGES, FAILED_MESSAGES
import logging
import json
from circuitbreaker import circuit

logger = logging.getLogger(__name__)
settings = get_settings()

class KafkaService:
    def __init__(self):
        self.producer = self._create_producer()
        self.consumer = None

    def _create_producer(self) -> KafkaProducer:
        return KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(2, 5, 0),
            retries=3
        )

    @circuit(failure_threshold=5, recovery_timeout=60)
    async def send_message(self, topic: str, data: Dict[str, Any]) -> bool:
        try:
            future = self.producer.send(topic, value=data)
            result = future.get(timeout=10)
            PROCESSED_MESSAGES.inc()
            logger.info(f"Message sent successfully: {data['device_id']}")
            return True
        except Exception as e:
            FAILED_MESSAGES.inc()
            logger.error(f"Failed to send message: {str(e)}")
            raise 