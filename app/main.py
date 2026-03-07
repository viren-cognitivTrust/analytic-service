from fastapi import FastAPI
import requests
from app.internal.store import EVENTS, add_event

app = FastAPI(title='analytics-service')
LOGGING_SERVICE_URL = 'http://logging-service:8012/log'


@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'analytics-service'}


@app.post('/events')
def ingest(event: dict):
    count = add_event(event)
    requests.post(LOGGING_SERVICE_URL, json=event, timeout=2)
    return {'stored': True, 'count': count}


@app.get('/events')
def list_events():
    return {'events': EVENTS}
