. venv/bin/activate
celery -A testServer.celery worker --concurrency 4 -E
deactivate
