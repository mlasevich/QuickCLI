'''
Sub Command
'''
import logging


LOG = logging.getLogger(__name__)


class QuickCLISubCommand(object):
    ''' QuickCLI SubCommand

    To be extended by end-user
    '''
    SUBCOMMANDS = []
    SUBCOMMAND_TITLE = "Sub Commands"
    SUBCOMMAND_DESC = "Sub Commands are commmands that are sub"
    SUBCOMMAND_META = "{cmd}"
    SUBCOMMAND_DEST_BASE = "action"
    SUBCOMMAND_DEST = None

    DESC = None

    def __init__(self, name, aliases=None, action=None):
        ''' Constructor '''
        self.aliases = aliases if aliases else []
        self.name = name
        self.action = action

    @property
    def desc(self):
        ''' Get Description for this subcommand '''
        if self.DESC:
            return self.DESC
        doc = self.__doc__
        if doc:
            return doc.strip().split('\n', 1)[0]
        return "???"

    def parser_args(self, parser):
        ''' Add Arguments to Parser '''
        return parser

    def process_args(self):
        ''' Process Arguments Hook'''

    def on_invalid_subcommand(self, subcommand_name, wrapper):
        ''' Hook executed if subcommand is invalid '''
        path = wrapper.path
        LOG.critical("Invalid subcommand '%s'%s",
                     subcommand_name, " for %s" % path if path else "")
        return 1

    def on_missing_subcommand(self, wrapper):
        ''' Hook executed if subcommand is not provided '''
        path = wrapper.delimited_path(":")
        LOG.critical("Must Specify Subcommand%s", " for action '%s'" %
                     path if path else "")
        return 1

    def prep_command(self, args, wrapper):
        ''' Executed before action to prepare command'''
        LOG.debug("Prep Command for %s - action: %s",
                  self.name, self.action != None)

    def execute(self, args, wrapper):
        ''' Execute Command '''
        LOG.debug("Execute Command for %s", self.name or "app")

        if self.action and callable(self.action):
            self.action(args)
