''' Unit Tests '''

import logging
import sys
import unittest

from .app_info import QuickCLIAppInfo, QuickCLIAppBaseInfo


__version__ = "version"
__date__ = "2019-01-02"
__updated__ = "2019-08-12"


def testvalue():
    ''' TestValue '''
    return "tester"


sys.modules['__main__'] = sys.modules[__name__]


class TestQuickCLI(unittest.TestCase):
    '''App Info tests'''

    def test_override_name(self):
        ''' Test pytest is installed '''
        class App(QuickCLIAppBaseInfo):
            ''' '''
            program_name = "myapp"

        app = App(program_name="override_name")
        self.assertEqual(app.info.program_name, "override_name")

    def test_default_name(self):
        ''' Test pytest is installed '''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App()
        self.assertEqual(app.info.program_name, "pytest")

    def test_invalid_items(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App()
        with self.assertRaises(AttributeError) as _context:
            app.info.program_name1

    def test_program_org(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App()
        self.assertEqual(app.info.program_org, "unknown")
        app = App(program_creator="creator")
        self.assertEqual(app.info.program_org, "creator")

    def test_program_version(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''
            program_version = "1.2.3"

        app = App()
        self.assertEqual(app.info.program_version, "1.2.3")
        app = App(program_version="1.0.2")
        self.assertEqual(app.info.program_version, "1.0.2")

    def test_program_version_module(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App()
        self.assertEqual(app.info.program_version, __version__)

    def test_program_version_function(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

            def program_version(self):
                ''' Generate Program Version '''
                return "x.y.z"

        app = App()
        self.assertEqual(app.info.program_version, "x.y.z")

    def test_program_build_date_module(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App()
        self.assertEqual(app.info.program_build_date, __updated__)

    def test_program_create_date_module(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App()
        self.assertEqual(app.info.program_create_date, __date__)

    def test_program_version_message(self):
        ''' Test invalid items'''
        class App(QuickCLIAppBaseInfo):
            ''' '''
            program_version = "X.Y.Z"
            program_build_date = "1234-56-78"

        app = App()
        self.assertEqual(app.info.program_version_message,
                         "%(prog)s vX.Y.Z (1234-56-78)")

    def test_program_shortdesc(self):
        ''' Test program_shortdesc'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App(program_copyright_year="2000", new_param="ex")
        self.assertEqual(app.info.program_shortdesc.strip(), "Unit Tests")
        self.assertEqual(app.info.program_copyright_year, "2000")

    def test_from_main(self):
        ''' Test from_main function'''
        class App(QuickCLIAppBaseInfo):
            ''' '''

        app = App(program_copyright_year="2000", new_param="ex")
        self.assertEqual(app.info.from_main('__version__'), __version__)
        self.assertEqual(app.info.from_main('testvalue'), "tester")
        self.assertIsNone(app.info.from_main('unset'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
