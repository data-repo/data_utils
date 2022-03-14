
import requests
from hashlib import md5
from typing import List
import rad_data.utils.helper as hp
from rad_data.utils.bunch import Bunch
from confluent_kafka import avro
from confluent_kafka import admin
import config as cfg 


class KafkaAdmin(object):
    """
    Kafka admin
    """
    def __init__(self) -> None:
        """
        Initialize Kafka admin class
        """
        self._admin = admin.AdminClient({
            'bootstrap.servers': ','.join(cfg.KAFKA_BOOTSTRAP_SERVERS)
        })

    def create_topic(self, topic) -> bool:
        """
        Create new topic in kafka
        """
        try:
            config = {
                "retention.ms": cfg.KAFKA_TOPIC_RETENTION_TIME,
                # "cleanup.policy": cfg.topic_cleanup_policy,
                # "auto.offset.reset": cfg.topic_auto_offset_reset,
                # "log.retention.bytes": cfg.topic_auto_offset_reset
                # "max.compaction.lag.ms": cfg.topic_max_compaction_lag_ms,
                # "min.compaction.lag.ms": cfg.topic_min_compaction_lag_ms
            }
            new_topic = admin.NewTopic(topic=topic,
                                                   num_partitions=cfg.KAFKA_TOPIC_NUM_PARTITIONS,
                                                   replication_factor=cfg.KAFKA_TOPIC_REPLICATION_FACTOR,
                                                   config=config)
            self._admin.create_topics([new_topic, ])
            print(f"Create topic {topic} successfully")
            return True
        except Exception as e:
            print(f"Create topic {topic} failed, {e}")
            return False

    def remove_topic(self, topics: List[str]) -> bool:
        """
        Delete topic from kafka
        """
        try:
            fs = self._admin.delete_topics(topics, operation_timeout=30)
            for topic, f in fs.items():
                try:
                    f.result()
                    print(f"Topic {topic} delete successfully")
                except Exception as e:
                    print(f"Delete {topic} topic failed, {e}")
        except Exception as e:
            print(f"Delete topic failed, {e}")
            return False


class KafkaAvroProducer(object):
    """
    Kafka avro data producer
    """

    def __init__(self, value_schema) -> None:
        """
        Initialize Kafka avro producer class
        """
        self._producer = None
        self._value_schema = value_schema
        self._key_schema = '{"type": "string"}'
        
    def __enter__(self):
        """
        Create kafka producer session
        """
        try:
            self._producer = avro.AvroProducer({
                'on_delivery': self.delivery_report,
                'schema.registry.url': cfg.KAFKA_SCHEMA_REGISTRY_URL,
                'bootstrap.servers': ','.join(cfg.KAFKA_BOOTSTRAP_SERVERS),
            }, default_key_schema=avro.loads(self._key_schema), default_value_schema=avro.loads(self._value_schema))
            return self
        except Exception as e:
            print(f'Can not connect to timescaledb data producer, {e}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close kafka producer connection
        """
        try:
            self._producer.flush()
        except Exception as e:
            print(f'Kafka data producer close connection is failed, {e}')

    @staticmethod
    def delivery_report(err, msg):
        """
        Called once for each message produced to indicate delivery result
        Triggered by poll() or flush()
        """
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def produce_batch_data(self, topic: str, keys: dict, docs: List[dict]) -> bool:
        """
        Produce list of messages to kafka topic
        """
        try:
            for doc in docs:
                if doc is not None:
                    key = '-'.join([self._hash_key(doc[key], value) for key, value in keys.items()])
                    self._producer.produce(topic=topic, value=doc, key=key)
            return True
        except Exception as e:
            print(f'Kafka batch data producer is failed, {e}')
            return False

    def produce_data(self, topic: str, keys: dict, doc: dict) -> bool:
        """
        Produce json object to kafka topic
        """
        try:
            print([self._hash_key(key_value=doc[key], key_type=value) for key, value in keys.items()])
            key = '-'.join([self._hash_key(key_value=doc[key], key_type=value) for key, value in keys.items()])
            self._producer.produce(topic=topic, key=key, value=doc)
            return True
        except Exception as e:
            print(f'Kafka data producer is failed, {e}')
            return False

    @staticmethod
    def _hash_key(key_value: str, key_type: str):
        """
        Hash key value
        """
        if key_type == 'md5':
            result = md5(key_value.encode())
            return result.hexdigest()
        else:
            return str(key_value)


class KafkaAvroConnector(object):
    """
    Kafka avro connector
    """
    def create_connector(self, name: str, topic: str, primary_key: str, db_name: str, table_name: str,
                         transforms: dict = None) -> bool:
        """
        Create connector and send data from kafka to database
        """
        try:
            schema_registry_url = cfg.KAFKA_SCHEMA_REGISTRY_URL
            connector_url = f'{cfg.KAFKA_CONNECTOR_URL}/connectors'
            timescale_connection_url = f'jdbc:postgresql://' \
                                       f'{cfg.TIMESCALEDB_GENERAL_HOST}:{cfg.TIMESCALEDB_GENERAL_PORT}/{db_name}?' \
                                       f'user={cfg.TIMESCALEDB_GENERAL_USERNAME}&' \
                                       f'password={cfg.TIMESCALEDB_GENERAL_PASSWORD}'
            headers = {
                "Content-Type": "application/json"
            }
            connector = {
                "name": name.upper(),
                "config": {
                    "topics": topic,
                    "pk.fields": primary_key,
                    "auto.create": "true",
                    "insert.mode": "upsert",
                    "pk.mode": "record_value",
                    "table.name.format": f"{table_name}",
                    "connection.url": timescale_connection_url,
                    "value.converter.schema.registry.url": schema_registry_url,
                    "value.converter": "io.confluent.connect.avro.AvroConverter",
                    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
                }
            }
            if transforms:
                connector['config'].update(
                    self._get_connector_transforms(transforms=transforms)
                )
            requests.post(url=connector_url, json=connector, headers=headers)
            return True
        except Exception as e:
            print(f'Kafka connect create connector failed, {e}')
            return False

    def remove_connector(self, name: str) -> bool:
        """
        Produce json object to kafka topic
        """
        try:
            connector_url = f'{cfg.KAFKA_CONNECTOR_URL}/connectors/{name}'
            requests.delete(url=connector_url)
            return True
        except Exception as e:
            print(f'Kafka connect create connector failed, {e}')
            return False

    @staticmethod
    def _get_connector_transforms(transforms: dict) -> dict:
        """
        Get kafka connect transforms
        """
        transform_names = []
        connector_transforms = {}
        for transform, operator in transforms.items():
            if transform == 'filter':
                key = list(operator.keys())[0]
                value = list(operator.values())[0]
                filter_name = "connectorFilter"
                connector_transforms.update({
                    f"transforms.{filter_name}.type": "io.confluent.connect.transforms.Filter$Value",
                    f"transforms.{filter_name}.filter.condition": f"$[?(@.{key} == '{value}')]",
                    f"transforms.{filter_name}.filter.type": "include",
                })
                transform_names.append(filter_name)
            elif transform == 'drop':
                drop_name = "connectorDrop"
                connector_transforms.update({
                    f"transforms.{drop_name}.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
                    f"transforms.{drop_name}.blacklist": ','.join(operator)
                })
                transform_names.append(drop_name)
        connector_transforms["transforms"] = ','.join(transform_names)
        return connector_transforms
