
import unittest
from rad_data.utils.checker import SiteBanChecker


class SiteBacCheckerTestCase(unittest.TestCase):

    def __init__(self, *args, ** kwargs):
        """
        Initialize site ban checker test case class
        """
        super(SiteBacCheckerTestCase, self).__init__(*args, **kwargs)
        self._site_ban = SiteBanChecker(config='test/config/ban.yml')

    def site_ban_checker(self):
        """
        Test ban checker
        """
        self._site_ban.check(max_workers=1)


if __name__ == '__main__':
    unittest.main()
