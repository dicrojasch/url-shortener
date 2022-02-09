from datetime import datetime

from __init__ import init_app
from services.kafka import create_topic, Consumer
from services.models import LogInternal
from settings.settings import get_config_dict_env
from loguru import logger


def save_log(json_message):
    date_event = json_message['date_event']
    type_event = json_message['type_event']
    short_link = json_message['short_link']
    long_link = json_message['long_link']
    type_client = json_message['type_client']
    date_event_final = datetime.fromtimestamp(date_event)
    log_internal = LogInternal(date_event=date_event_final, type_event=type_event, short_link=short_link, long_link=long_link, type_client=type_client)
    log_internal.save()


config = init_app()

logger.info("configuration loaded")
logger.info(config)

topic = config["KAFKA_TOPIC"]
host = config["KAFKA_HOST"]
port = config["KAFKA_PORT"]
auto_offset_reset = config["KAFKA_OFFSET_RESET"]
consumer_timeout = config["KAFKA_TIMEOUT"]

logger.info("Starting kafka consumer...")
consumer = Consumer(topic, host, port, auto_offset_reset, consumer_timeout, save_log)
consumer.run()

