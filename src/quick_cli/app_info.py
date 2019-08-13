''' App Info Classes '''
from datetime import datetime
import os.path
import sys


class QuickCLIAppInfo(object):
    ''' Application Info '''

    INFO = {
        'program_name': 'prog',
        'program_version': '0.0.0',
        'program_build_date': 'unknown',
        'program_create_date': 'unknown',
        'program_version_message': '%%(prog)s',
        'program_shortdesc': 'Short Description',
        'program_creator': 'unknown',
        'program_org': 'unknown',
        'program_copyright_year': datetime.now().year,
        'program_license_desc': '''
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

''',
        'program_desc': "Usage:",
        'program_epilog': "Thats All Folks"
    }

    def __init__(self, app, **kwargs):
        ''' Constructor '''
        self.app = app
        self.info = {}
        for item, value in kwargs.items():
            if item in self.INFO:
                self.info[item] = value

    def from_main(self, key, default_value=None):
        ''' Get key from '''
        main = sys.modules['__main__']
        item = getattr(main, key, default_value)
        if callable(item):
            return item()
        return item

    def __getattr__(self, name):
        ''' Get attribute by name '''
        if name not in self.INFO:
            raise AttributeError("Invalid App Info item '%s'" % name)
        if name in self.info:
            return self.info[name]

        default_value_base = self.INFO.get(name, '--')
        # Get default_value from app, if exists
        default_value = getattr(self.app, "%s_default" %
                                name.lower(), default_value_base)

        try:
            getter = getattr(self.app, name.lower())
            if callable(getter):
                return getter()
            if getter:
                return getter
        except AttributeError:
            pass

        return default_value if not callable(default_value) else default_value(default_value_base)


class QuickCLIAppBaseInfo(object):
    ''' Base for QuickCLIApp Class for Info '''

    def __init__(self, **kwargs):
        ''' Constructor '''
        self.info = QuickCLIAppInfo(self, **kwargs)

    def program_name_default(self, default_value):
        ''' Get Program Name '''
        name = os.path.basename(sys.argv[0])
        if name:
            if name.endswith('.py'):
                return name[:-3]
            return name
        return default_value

    def program_org_default(self, default_value):
        '''  Program Organization Default '''
        return self.info.program_creator

    def program_version_default(self, default_value):
        ''' Program Version Default '''
        return self.info.from_main('__version__', default_value)

    def program_build_date_default(self, default_value):
        ''' Program create Date Default '''
        return self.info.from_main('__updated__', default_value)

    def program_create_date_default(self, default_value):
        ''' Program Build Date Default '''
        return self.info.from_main('__date__', default_value)

    def program_version_message_default(self, default_value):
        return '%%(prog)s v%s (%s)' % (self.info.program_version, self.info.program_build_date)

    def program_shortdesc_default(self, default_value):
        ''' Get program short description Default '''
        docstring = self.info.from_main('__doc__', None)

        if docstring:
            return docstring.split("\n")[1] if '\n' in docstring else docstring

        return self.info.program_name

    def program_desc_default(self, default_value):
        ''' Get Desc Default '''
        return '''%s

  Created by %s on %s.
  Copyright %s %s. All rights reserved.

%s
USAGE
''' % (
            self.info.program_shortdesc,
            self.info.program_creator,
            self.info.program_create_date,
            self.info.program_copyright_year,
            self.info.program_org,
            self.info.program_license_desc)
