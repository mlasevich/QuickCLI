''' QuickCLI Context '''
import logging


LOG = logging.getLogger(__name__)


class QuickCLIContextConfig(object):
    ''' Application Context Config '''
    PARAMS = {
        'allow_unset': (bool, True),
        'unset_value': (str, '')
    }

    def __init__(self, context, **kwargs):
        ''' Constructor '''
        self.context = context
        self.config = dict(kwargs)

    def __getattr__(self, name):
        ''' Get Attribute '''
        if name in QuickCLIContextConfig.PARAMS:
            return self.config.get(name, QuickCLIContextConfig.PARAMS[name][1])
        raise AttributeError(
            "No Such Attribute '%s' in QuickCLIContextConfig" % name)


class QuickCLIContext(object):
    ''' Application Context '''

    def __init__(self, app=None, config=None, **kwargs):
        ''' Constructor for context '''
        self._app = app
        config = config if config is not None else {}
        if isinstance(config, QuickCLIContextConfig):
            self._config = config
        elif isinstance(config, dict):
            self._config = QuickCLIContextConfig(self, **config)
        else:
            LOG.warning(
                "Invalid type for QuickCLIContext config: %s", type(config))
            self._config = QuickCLIContextConfig(self)
        self.data = dict(kwargs)

    def update(self, context):
        ''' Update context from a dictinary '''
        if context is None:
            return
        if isinstance(context, dict):
            self.data.update(context)
        else:
            print("Invalid data type '%s', unable to update context", type(context))

    @property
    def app(self):
        ''' Get application '''
        return self._app

    @app.setter
    def app(self, app):
        ''' Set application '''
        self._app = app

    def set(self, key, value):
        ''' Set value in context '''
        self.data[key] = value

    def setdefault(self, key, value):
        ''' Set value if not already set. Return value '''
        if key not in self.data:
            print("initializing %s in context" % key)
            self.data[key] = value
        return self.get(key)

    def get(self, key, default_value=None):
        ''' Get Value from Context '''
        value = self.data.get(key, default_value)
        return value

    def __repr__(self):
        ''' Representation of this context '''
        return "{Context::%s}" % self.data

    def __getattr__(self, name):
        ''' Get context attribute '''
        if name in self.data:
            return self.data.get(name, None)
        elif self._config.allow_unset:
            return self._config.unset_value
        raise AttributeError("Invalid QuickCLIContext attribute '%s' " % name)

    def __len__(self):
        ''' Number of Context Items '''
        return len(self.data)

    def __getitem__(self, key):
        ''' Get item by index key '''
        return self.data.get(key, self.config.unset_value)

    def __setitem__(self, key, value):
        ''' Set context item by index key '''
        self.data[key] = value

    def __delitem__(self, key):
        ''' Del item by index key '''
        if key in self.data:
            del self.data[key]

    def __iter__(self):
        ''' Iterator for context data '''
        return self.data.__iter__()

    def __contains__(self, item):
        ''' Check if  item is in context '''
        return item in self.data

    def __missing__(self, item):
        ''' Check if item is not in context '''
        return not self.__contains__(item)
