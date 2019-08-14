''' Actions '''
import logging

LOG = logging.getLogger(__name__)


class ActionBase(object):
    ''' QuickCLI SubCommand Action

    May Be extended by end-user
    '''

    ACTIONS = []
    ACTIONS_TITLE = "Sub Action"
    ACTIONS_DESC = "Available Actions"
    ACTIONS_METAVAR = "{action}"
    ACTIONS_DEST_BASE = "action"
    ACTIONS_DEST = None

    DESC = None

    def __init__(self, name, aliases=None, **kwargs):
        ''' Constructor '''
        self.aliases = aliases if aliases else []
        self.name = name
        self._properties = kwargs

    def _get_property(self, paramname, fixed_paramname=None, default_value=None):
        ''' Get property from _properties '''
        if fixed_paramname is None:
            fixed_paramname = paramname.upper()
        if paramname in self._properties:
            return self._properties[paramname]
        if fixed_paramname:
            return getattr(self, fixed_paramname, default_value)
        return default_value

    @property
    def actions(self):
        ''' Get SubCommands '''
        return self._get_property('actions', default_value=[])

    @property
    def actions_title(self):
        ''' Get SubCommands '''
        return self._get_property('actions_title', default_value="actions")

    @property
    def actions_desc(self):
        ''' Get Action Description '''
        return self._get_property('actions_desc', default_value="Available Actions")

    @property
    def actions_metavar(self):
        ''' Get Action Metavar '''
        return self._get_property('actions_metavar', default_value="{action}")

    @property
    def actions_dest_base(self):
        ''' Get Action Destination Variable Base '''
        return self._get_property('actions_dest_base', default_value="action")

    @property
    def actions_dest(self):
        ''' Get Action Destination Variable '''
        return self._get_property('actions_dest', default_value=None)

    @property
    def desc(self):
        ''' Get Description for this action '''
        desc = self._get_property('desc', default_value=None)
        if desc is not None:
            return desc
        doc = self.__doc__
        if doc:
            return doc.strip().split('\n', 1)[0]
        return "No description"

    def parser_args(self, parser):
        ''' Add Arguments to Parser '''
        return parser

    def process_args(self):
        ''' Process Arguments Hook'''

    def on_invalid_action(self, action_name, wrapper):
        ''' Hook executed if action is invalid '''
        path = wrapper.path
        LOG.critical("Invalid %s '%s'%s", self.actions_title,
                     action_name, " for %s" % path if path else "")
        return 1

    def on_missing_action(self, wrapper):
        ''' Hook executed if action is not provided '''
        path = wrapper.delimited_path(":")
        LOG.critical("Must Specify Action%s", " for action '%s'" %
                     path if path else "")
        return 1

    def prep_command(self, args, wrapper):
        ''' Executed before action to prepare command'''
        prep_command = self._get_property(
            "prep_command", "", default_value=None)
        if prep_command and callable(prep_command):
            LOG.debug("Prep Command for %s - action: %s",
                      self.name, prep_command != None)
            return prep_command(args, wrapper)
        LOG.debug("Prep Command for %s - action: %s",
                  self.name, prep_command != None)

    def execute(self, args, wrapper):
        ''' Executed action'''
        action = self._get_property("action", "", default_value=None)
        if action and callable(action):
            LOG.debug("Action for %s - action: %s", self.name, action != None)
            return action(args, wrapper)
        LOG.debug("Action for %s - action: %s", self.name, action != None)
        return -1


class Action(ActionBase):
    ''' Generic Action '''

    def __init__(self, name, aliases=None, **kwargs):
        ActionBase.__init__(self, name, aliases=aliases, **kwargs)
