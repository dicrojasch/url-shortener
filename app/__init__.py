import os
from flask import Flask

from app.services.models import URLShortener
from app.services.zookeeper import ZookeeperURL
from app.settings.logging import set_logging
from app.settings.settings import BaseConfig, get_config_class_env
from app.utils import constants


def create_app():
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
    app.logger.info(" the range obtained for assignments is [" + str(app.config["START_NUMBER_RANGE"] - constants.RANGE_CAPACITY) + " - " + str(app.config["START_NUMBER_RANGE"]) + "]")
    zk_url.zk.stop()
    app.logger.info("------------------------------------------------------------")
    app.logger.info("-------------------------set-db-----------------------------")
    if not URLShortener.exists():
        app.logger.info("User Table does not exist, creating one...")
        URLShortener.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    app.logger.info("------------------------------------------------------------")

    app.logger.info("--------------------final-configurations--------------------")
    app.logger.info(app.config)
    app.logger.info("------------------------------------------------------------")

    return app
