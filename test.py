import unittest
import cron
from datetime import datetime

class TestCron(unittest.TestCase):

    def test_every_minute(self):
        self.assertEqual(cron.isToRun(datetime(2023, 9, 14, 23, 40),
          "* * * * *"), True)

if __name__ == '__main__':
    unittest.main()