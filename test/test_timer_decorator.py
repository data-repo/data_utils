
import time
import unittest
from rad_data.utils.logger import Logger
from rad_data.utils.decorator import timer

logger = Logger(config='test/config/logger.yml')


class TimerDecoratorTestCase(unittest.TestCase):

    @timer
    def test_timer(self):
        """
        Test timer
        """
        logger.info(msg='Test timer success')

    @timer(threshold_time=1000, logger=logger)
    def test_timer_threshold_time_and_logger(self):
        """
        Test timer threshold time and logger
        """
        time.sleep(2)
        logger.info('Test threshold time parameter success.')


if __name__ == '__main__':
    unittest.main()
