import os
from dotenv import load_dotenv

load_dotenv(".env_var")

class Config:

    # Celery setup
    CELERY_BROKER_URL=os.environ.get('CELERY_BROKER_URL'),
    CELERY_RESULT_BACKEND=os.environ.get('CELERY_RESULT_BACKEND')
    ALLOW_MULTIPLE_QUEUE = os.environ.get('ALLOW_MULTIPLE_QUEUE') == "true"
    HARD_TIME_LIMIT = int(os.environ.get('HARD_TIME_LIMIT_PER_TASK'))
    RESULT_EXPIRE_TIME = int(os.environ.get('RESULT_EXPIRE_TIME'))

    MAX_DURATION_MS = int(os.environ.get('MAX_DURATION_MS'))
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS').split(",")
