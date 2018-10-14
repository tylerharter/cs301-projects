. venv/bin/activate
celery -A testServer.celery worker --concurrency 1 -E
deactivate
