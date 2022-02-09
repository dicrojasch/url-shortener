import os

from app.utils import constants


class BaseConfig(object):
    """Base config, uses staging database server."""
    TESTING = False
    RANGE_CAPACITY = 10000


class ProductionBaseConfig(BaseConfig):
    """Uses production database server."""
    ZK_HOST = "zookeeper"
    ZK_PORT = "2181"
    DYNDB_HOST = "dynamodb-local"
    DYNDB_PORT = "8000"
    DYNDB_KEY = "anything"
    DYNDB_SECRET = "fake"
    REGION = 'us-west-1'
    DYNDB_TABLE_LINK = "link"
    DYNDB_TABLE_LOG = "log_internal"
    KAFKA_TOPIC = "log_topic"
    KAFKA_HOST = "kafka"
    KAFKA_PORT = "9092"
    KAFKA_PARTITION = 1
    KAFKA_REP_FACTOR = 1
    URL_PUBLIC = "https://239m52oz3g.execute-api.us-east-1.amazonaws.com/"


class DevelopmentLocalBaseConfig(BaseConfig):
    ZK_HOST = "127.0.0.1"
    ZK_PORT = "2181"
    DYNDB_HOST = "127.0.0.1"
    DYNDB_PORT = "8000"
    DYNDB_KEY = "anything"
    DYNDB_SECRET = "fake"
    REGION = 'us-west-1'
    DYNDB_TABLE_LINK = "link"
    DYNDB_TABLE_LOG = "log_internal"
    KAFKA_TOPIC = "log_topic"
    KAFKA_HOST = "localhost"
    KAFKA_PORT = "9092"
    KAFKA_PARTITION = 1
    KAFKA_REP_FACTOR = 1


class DevelopmentDockerBaseConfig(BaseConfig):
    ZK_HOST = "zookeeper"
    ZK_PORT = "2181"
    DYNDB_HOST = "dynamodb-local"
    DYNDB_PORT = "8000"
    DYNDB_KEY = "anything"
    DYNDB_SECRET = "fake"
    REGION = 'us-west-1'
    DYNDB_TABLE_LINK = "link"
    DYNDB_TABLE_LOG = "log_internal"
    KAFKA_TOPIC = "log_topic"
    KAFKA_HOST = "kafka"
    KAFKA_PORT = "9092"
    KAFKA_PARTITION = 1
    KAFKA_REP_FACTOR = 1


def get_config_class_env():
    env_type_deploy = os.environ.get(constants.DEPLOY_TYPE)
    if env_type_deploy == constants.DEVELOP_LOCAL:
        return DevelopmentLocalBaseConfig
    elif env_type_deploy == constants.DEVELOP_DOCKER:
        return DevelopmentDockerBaseConfig

    return ProductionBaseConfig


def get_config_dict_env():
    return get_config_class_env().__dict__