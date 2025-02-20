from prometheus_client import Counter, start_http_server
from app.core.config import get_settings

settings = get_settings()

# Define metrics
PROCESSED_MESSAGES = Counter('processed_messages_total', 'Number of processed messages')
FAILED_MESSAGES = Counter('failed_messages_total', 'Number of failed messages')

def setup_metrics():
    if settings.ENABLE_METRICS:
        start_http_server(settings.METRICS_PORT) 