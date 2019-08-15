''' Unit Tests For Actions '''

import logging
import unittest

from .actions import ActionBase


def dummy_action():
    ''' Test '''


class TestQuickCLIActions(unittest.TestCase):
    '''App Info tests'''

    def test_actions_desc_override(self):
        ''' Test getting action_desc'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], actions_desc="mydesc", action=dummy_action)
        self.assertEqual(action.actions_desc, "mydesc")

    def test_actions_base_default(self):
        ''' Test getting action_desc'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], action=dummy_action)
        self.assertEqual(action.actions_desc, "Available Actions")

    def test_actions_dest_override(self):
        ''' Test getting action_dest'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], actions_dest="mydest", action=dummy_action)
        self.assertEqual(action.actions_dest, "mydest")

    def test_actions_dest_default(self):
        ''' Test getting action_dest'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], action=dummy_action)
        self.assertIsNone(action.actions_dest)

    def test_actions_dest_base_override(self):
        ''' Test getting action_dest_base'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], actions_dest_base="mydest_base", action=dummy_action)
        self.assertEqual(action.actions_dest_base, "mydest_base")

    def test_actions_dest_base_default(self):
        ''' Test getting action_dest_base'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], action=dummy_action)
        self.assertEqual(action.actions_dest_base, 'action')

    def test_actions_metavar_override(self):
        ''' Test getting action_metavar'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], actions_metavar="my_meta", action=dummy_action)
        self.assertEqual(action.actions_metavar, "my_meta")

    def test_actions_metavar_default(self):
        ''' Test getting action_metava'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], action=dummy_action)
        self.assertEqual(action.actions_metavar, "{action}")

    def test_desc_default(self):
        ''' Test getting action_desc'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], action=dummy_action)
        self.assertEqual(action.desc, "QuickCLI SubCommand Action")

    def test_desc_override(self):
        ''' Test getting action_dest'''
        action = ActionBase(name="name", aliases=[
                            'alias1', 'alias2'], desc="my desc", action=dummy_action)
        self.assertEqual(action.desc, "my desc")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
