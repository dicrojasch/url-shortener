import json

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


class Producer:
    def __init__(self, topic, host, port):
        self.topic = topic
        self.host = host
        self.port = port
        self.host_port = self.host + ':' + self.port

    def send_event(self, date_event, type_event, short_link, long_link, type_client):
        producer = KafkaProducer(bootstrap_servers=self.host_port)
        record = {'date_event': date_event,
                  'type_event': type_event,
                  'short_link': short_link,
                  'long_link': long_link,
                  'type_client': type_client
                  }
        record_bytes = json.dumps(record).encode('utf-8')
        producer.send(self.topic, record_bytes)

        producer.flush()
        producer.close()


def create_topic(topic_, host_, port_, num_partitions_, replication_factor_):
    try:
        host_port = host_ + ':' + port_
        admin = KafkaAdminClient(bootstrap_servers=host_port)

        topic_create = NewTopic(name=topic_,
                                num_partitions=num_partitions_,
                                replication_factor=replication_factor_)

        admin.create_topics([topic_create])
    except TopicAlreadyExistsError as e:
        print("Topic already exists.")
        pass
