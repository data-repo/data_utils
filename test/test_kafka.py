
import unittest
from rad_data.utils.kafka import KafkaDataProducer


class KafkaTestCase(unittest.TestCase):

    def __init__(self, *args, ** kwargs):
        """
        Initialize kafka test case class
        """
        super(KafkaTestCase, self).__init__(*args, **kwargs)
        self._config_path = 'config/kafka.yml'

    def test_kafka_data_producer(self):
        """
        Test kafka data producer
        """
        with KafkaDataProducer(config=self._config_path) as kafka:
            self.assertTrue(
                kafka.produce_data(doc={
                    'data': 'Send data from base kafka producer class'
                }, topic='test')
            )

    def test_kafka_batch_date_producer(self):
        """
        Test kafka batch data producer
        """
        with KafkaDataProducer(config=self._config_path) as kafka:
            self.assertTrue(
                kafka.produce_batch_data(
                    docs=[
                        {'batch_data_one': 'Send batch data one from base kafka producer class'},
                        {'batch_data_two': 'Send batch data two from base kafka producer class'}
                    ], topic='test')
            )


if __name__ == '__main__':
    unittest.main()
