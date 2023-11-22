import os
from celery import Celery
from config import Config
from transcribe import Transcriber

transcriber = Transcriber()

HARD_TIME_LIMIT=Config.HARD_TIME_LIMIT

celery = Celery("server",
                broker=Config.CELERY_BROKER_URL,
                backend=Config.CELERY_RESULT_BACKEND,
                result_expires=Config.RESULT_EXPIRE_TIME
                )

@celery.task(queue="long_audio", time_limit=HARD_TIME_LIMIT)
def long_running_tasks(audio_path):
    return transcriber.transcribe(audio_path)

@celery.task(queue="short_audio", time_limit=HARD_TIME_LIMIT)
def short_running_tasks(audio_path):
    return transcriber.transcribe(audio_path)
        
