''' Unit Tests For Actions '''

import logging
import sys
import unittest

from .actions import ActionBase


def dummy_action():
    ''' Test '''


class TestQuickCLIActions(unittest.TestCase):
    '''App Info tests'''

    # def test_actions_base(self):
    #    ''' Test getting action_desc'''
    #    action = ActionBase(name="name", aliases=[
    #                        'alias1', 'alias2'], action_desc="mydesc", action=dummy_action)
    #    self.assertEqual(action.actions_desc, "mydesc")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
