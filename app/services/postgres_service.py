import psycopg2
from psycopg2.extras import DictCursor
from app.core.config import get_settings
import logging
import platform

logger = logging.getLogger(__name__)
settings = get_settings()

class PostgresService:
    def __init__(self):
        # Adjust host for macOS
        host = 'localhost' if platform.system() == 'Darwin' else settings.POSTGRES_HOST
        
        self.connection_params = {
            'dbname': settings.POSTGRES_DB,
            'user': settings.POSTGRES_USER,
            'password': settings.POSTGRES_PASSWORD,
            'host': host,
            'port': settings.POSTGRES_PORT
        }

    def get_connection(self):
        return psycopg2.connect(**self.connection_params)

    async def store_sensor_data(self, data):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO sensor_metrics 
                        (device_id, temperature_f, pressure_psi, timestamp)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        data['device_id'],
                        data['temperature_f'],
                        data['pressure_psi'],
                        data['timestamp']
                    ))
                    conn.commit()
            logger.info(f"Stored sensor data for device: {data['device_id']}")
            return True
        except Exception as e:
            logger.error(f"Failed to store sensor data: {str(e)}")
            raise 