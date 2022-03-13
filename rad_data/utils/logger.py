
import os
import json
import inspect
from enum import Enum
from rad_data.utils.kafka import KafkaAvroProducer
from rad_data.utils.bunch import Bunch
from datetime import datetime
from dataclasses import dataclass
from rad_data.utils.kafka import KafkaAvroConnector
from dataclasses_avroschema import AvroModel
import rad_data.utils.helper as hp
import config as cfg
import confluent_kafka.admin as kafka_admin

@dataclass
class LoggerModel(AvroModel):
    """
    schedule time: 24h
    primary key: utc_timestamp,app_name
    """

    pid: int
    level: str
    message: str
    file: str
    function: str
    utc_timestamp: datetime

    class Meta:
        namespace = 'logs.v1'

    @staticmethod
    def table_name():
        return 'logs'

    @staticmethod
    def create_connector():
        """
        Create coins table connector
        """
        connector = KafkaAvroConnector()
        return connector.create_connector(topic='logs', name="LOG_CONNECTOR",
                                          primary_key="utc_timestamp,app_name", db_name='logs')

    @staticmethod
    def delete_connector():
        """
        Create logs table connector
        """
        connector = KafkaAvroConnector()
        connector.remove_connector(name=f"LOG_CONNECTOR")

    @staticmethod
    def create_table() -> bool:
        """
        Create the coins table schema
        """
        pass

    @staticmethod
    def delete_table():
        """
        Create the logs table schema
        """
        pass

    @staticmethod
    def delete_topic():
        """
        Delete logs topics from kafka
        """
        conf = {
            'bootstrap.servers':
                cfg.KAFKA_BOOTSTRAP_SERVERS
        }
        kafka_client = kafka_admin.AdminClient(conf=conf)
        topics = ['logs']

        try:
            fs = kafka_client.delete_topics(topics, operation_timeout=30)
            for topic, s in fs.items():
                try:
                    s.result()
                    print(f"Topic {topic} deleted")
                except Exception as e:
                    print(f"Failed to delete topic {topic}: {e}")
        except Exception as e:
            print(e)


class LoggerFormat(Enum):
    """
    Enum for logger formats
    """
    JSON = 0
    STRING = 1


class LoggerLevel(Enum):
    """
    Enum for logger levels
    """
    NOTSET = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logger(object):
    """
    Log string and messages on kafka
    """

    def __init__(self) -> None:
        """
        Initialize logger class
        Args:
            config: Get logger config by file path or bunch object
        """
        level = cfg.LOGGER_LEVEL.upper()
        self._log_level = LoggerLevel[level] if level in LoggerLevel.__members__ else LoggerLevel.NOTSET

    def log(self, level: str, msg: str, **kwargs) -> bool:
        """
        Log messages with different levels
        Args:
            level: Log level
            msg: Log message
            **kwargs: More parameters for logging message
        Returns: Log string message or log message on kafka message broker
        """
        if 'func' in kwargs:
            func_object = kwargs['func']
            file = inspect.getfile(func_object)
            func = func_object.__name__
        else:
            file = inspect.stack()[2].filename
            func = inspect.stack()[2].function
        pid = os.getpid()
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        if LoggerLevel[level].value >= self._log_level.value:
            logger_format = cfg.LOGGER_FORMAT.lower()
            if logger_format == LoggerFormat.JSON.name.lower():
                doc = {
                    'app_name': cfg.APP_NAME,
                    'pid': pid,
                    'level': level,
                    'message': msg,
                    'file': file,
                    'function': func,
                    'utc_timestamp': hp.datetime_to_unix(log_time, date_time_format='%Y-%m-%d %H:%M:%S')
                }
                topic = LoggerModel.table_name()
                with KafkaAvroProducer(value_schema=LoggerModel.avro_schema()) as kafka:
                    kafka.produce_data(doc=doc, topic=topic, keys={'utc_timestamp': int,'app_name':cfg.APP_NAME})
                print(f'{pid} - {log_time} {level} | message: {msg}, file: {file}, function: {func}')
                return True
            elif logger_format == LoggerFormat.STRING.name.lower():
                print(f'{pid} - {log_time} {level} | message: {msg}, file: {file}, function: {func}')
                return True
            else:
                print('Logger format is not correct!')
                return False

    def debug(self, msg: str, **kwargs) -> bool:
        """
        Log debug message
        Args:
            msg: Log message
            **kwargs: More parameters for debug message
        Returns: Log debug massage based on string or json type
        """
        return self.log(level=LoggerLevel.DEBUG.name, msg=msg, **kwargs)

    def info(self, msg: str, **kwargs) -> bool:
        """
        Log info message
        Args:
            msg: Log message
            **kwargs: More parameters for info message
        Returns: Log info massage based on string or json type
        """
        return self.log(level=LoggerLevel.INFO.name, msg=msg, **kwargs)

    def error(self, msg: str, **kwargs) -> bool:
        """
        Log error message
        Args:
            msg: Log message
            **kwargs: More parameters for error message
        Returns: Log error massage based on string or json type
        """
        return self.log(level=LoggerLevel.ERROR.name, msg=msg, **kwargs)

    def warning(self, msg: str, **kwargs) -> bool:
        """
        Log warning message
        Args:
            msg: Log message
            **kwargs: More parameters for warning message
        Returns: Log warning massage based on string or json type
        """
        return self.log(level=LoggerLevel.WARNING.name, msg=msg, **kwargs)

    def critical(self, msg: str, **kwargs) -> bool:
        """
        Log critical message
        Args:
            msg: Log message
            **kwargs: More parameters for critical message
        Returns: Log critical massage based on string or json type
        """
        return self.log(level=LoggerLevel.CRITICAL.name, msg=msg, **kwargs)
