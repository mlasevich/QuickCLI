''' Unit Tests '''

import logging
import unittest


class TestQuickCLI(unittest.TestCase):
    """Config unit test stubs"""

    def test_pytest(self):
        ''' Test pytest is installed '''
        actual = True
        self.assertTrue(actual)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
