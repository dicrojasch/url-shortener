from loguru import logger

from services.models import LogInternal
from services.kafka import create_topic
from settings.settings import get_config_dict_env


def init_app():
    config = get_config_dict_env()
    logger.info("parameters loaded:")
    logger.info(config)

    dynDBTable = config["DYNDB_TABLE_LOG"]

    topic = config["KAFKA_TOPIC"]
    host = config["KAFKA_HOST"]
    port = config["KAFKA_PORT"]
    num_partitions = config["KAFKA_PARTITION"]
    replication_factor = config["KAFKA_REP_FACTOR"]

    logger.info("creating kafka topic '" + topic + "':")
    create_topic(topic, host, port, num_partitions, replication_factor)

    logger.info("creating dynamodb table '" + dynDBTable + "':")
    if not LogInternal.exists():
        logger.info("'" + dynDBTable + "' Table does not exist, creating one...")
        LogInternal.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    else:
        logger.info("Table '" + dynDBTable + "' already exists")

    return config
