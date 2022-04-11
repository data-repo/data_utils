
import unittest
from data_tools.utils.logger import Logger


class LoggerTestCase(unittest.TestCase):

    def __init__(self, *args, ** kwargs):
        """
        Initialize logger test case class
        """
        super(LoggerTestCase, self).__init__(*args, **kwargs)
        self._logger = Logger(config='test/config/logger.yml')

    def test_debug_log(self):
        """
        Test debug log
        """
        self._logger.debug(msg='Test debug logger in unit test')

    def test_info_log(self):
        """
        Test info log
        """
        self._logger.info(msg='Test info logger in unit test')

    def test_warning_log(self):
        """
        Test warning log
        """
        self._logger.warning(msg='Test warning logger in unit test')

    def test_error_log(self):
        """
        Test error log
        """
        self._logger.error(msg='Test error logger in unit test')

    def test_critical_log(self):
        """
        Test critical log
        """
        self._logger.critical(msg='Test critical logger in unit test')


if __name__ == '__main__':
    unittest.main()
