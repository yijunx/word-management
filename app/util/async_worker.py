from celery import Celery
from app.config.app_config import conf
from enum import Enum


celery = Celery(conf.CELERY_SERVICE_NAME, broker=conf.CELERY_BROKER)


class CeleryTaskEnum(str, Enum):
    send_suggestion_notice = "send_suggestion_notice"
