import json
import threading
from datetime import datetime

from kafka import KafkaConsumer
from kafka.errors import TopicAlreadyExistsError

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from loguru import logger


class Consumer(threading.Thread):
    def __init__(self, topic, host, port, offset_reset, timeout, method_on_receive):
        threading.Thread.__init__(self)
        self.topic = topic
        self.host = host
        self.port = port
        self.host_port = self.host + ':' + self.port
        self.offset_reset = offset_reset
        self.timeout = timeout
        self.method_on_receive = method_on_receive
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer_kafka = KafkaConsumer(bootstrap_servers=self.host_port,
                                       auto_offset_reset=self.offset_reset,
                                       consumer_timeout_ms=self.timeout)
        consumer_kafka.subscribe([self.topic])
        logger.info("Kafka consume started, listening...")
        while not self.stop_event.is_set():
            for message in consumer_kafka:
                if message:
                    logger.info("message received.")
                    logger.info("   " + str(message))
                    message_json = json.loads(message.value)
                    self.method_on_receive(message_json)

                if self.stop_event.is_set():
                    break

        consumer_kafka.close()


def create_topic(topic_, host_, port_, num_partitions_, replication_factor_):
    try:
        host_port = host_ + ':' + port_
        admin = KafkaAdminClient(bootstrap_servers=host_port)

        topic_create = NewTopic(name=topic_,
                                num_partitions=num_partitions_,
                                replication_factor=replication_factor_)

        admin.create_topics([topic_create])
    except TopicAlreadyExistsError as e:
        logger.info("Topic already exists.")
        pass

