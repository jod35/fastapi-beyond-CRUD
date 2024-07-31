
celery -A src.celery_tasks.c_app worker &

celery -A src.celery_tasks.c_app flower