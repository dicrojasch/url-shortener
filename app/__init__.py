import os
from flask import Flask

from app.services.kafka import Producer, create_topic
from app.services.models import URLShortener
from app.services.zookeeper import ZookeeperURL
from app.settings.logging import set_logging
from app.settings.settings import BaseConfig, get_config_class_env
from app.utils import constants


def init_app():
    app = Flask(__name__)
    env = app.config["ENV"]
    app.config.from_object(BaseConfig)
    app.config.from_object(get_config_class_env())
    app.secret_key = os.urandom(12)
    set_logging()
    app.logger.info("-------------set-zookeeper-for-coordination----------------")
    app.logger.info(" getting range for url assigments... ")
    zk_url = ZookeeperURL(app.config["ZK_HOST"], app.config["ZK_PORT"])
    zk_url.zk.start()
    app.config["START_NUMBER_RANGE"] = zk_url.get_range()
    app.config["FINAL_NUMBER_RANGE"] = app.config["START_NUMBER_RANGE"] + constants.RANGE_CAPACITY
    app.config["APPLICATION_ID_ZK"] = app.config["START_NUMBER_RANGE"]
    app.logger.info(" the range obtained for assignments is [" + str(app.config["START_NUMBER_RANGE"]) + " - " + str(app.config["FINAL_NUMBER_RANGE"]) + "]")
    zk_url.zk.stop()
    app.logger.info("------------------------------------------------------------")
    app.logger.info("-------------------------set-db-----------------------------")
    table_name = app.config["DYNDB_TABLE_LINK"]
    app.logger.info("creating dynamodb table '" + table_name + "':")
    if not URLShortener.exists():
        app.logger.info("'" + table_name + "' Table does not exist, creating one...")
        URLShortener.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    app.logger.info("------------------------------------------------------------")

    app.logger.info("-------------------------kafka-conf-------------------------")
    topic = app.config["KAFKA_TOPIC"]
    host = app.config["KAFKA_HOST"]
    port = app.config["KAFKA_PORT"]
    num_partitions = app.config["KAFKA_PARTITION"]
    replication_factor = app.config["KAFKA_REP_FACTOR"]
    create_topic(topic, host, port, num_partitions, replication_factor)
    app.logger.info("------------------------------------------------------------")

    app.logger.info("--------------------final-configurations--------------------")
    app.logger.info(app.config)
    app.logger.info("------------------------------------------------------------")
    app.logger.info(" set up ready, listening request...")

    return app
