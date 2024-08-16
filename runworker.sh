
celery -A src.celery_tasks.c_app worker --loglevel=INFO &

celery -A src.celery_tasks.c_app flower