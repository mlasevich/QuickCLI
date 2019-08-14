''' 
Action Wrapper
'''
import logging
import sys

LOG = logging.getLogger(__name__)

IS_PYTHON2 = sys.version_info[0] == 2


class ActionWrapper(object):

    def __init__(self, command, parent):
        ''' Constructor for Command Wrapper '''
        self.command = command
        self.parent = parent
        self.app = self.root.command

        self.actions = []
        self.actions_idx = {}
        self._process_actions(command.actions)

    def _process_actions(self, actions):
        ''' Process actions '''
        for action in actions:
            wrapped = ActionWrapper(action, self)
            self.actions.append(wrapped)
            self.actions_idx[action.name] = wrapped
        for wrapped in self.actions:
            for alias in wrapped.aliases:
                if not alias in self.actions_idx:
                    self.actions_idx[alias] = wrapped

    @property
    def has_actions(self):
        ''' Check if we have sub-commands '''
        return True if self.actions else False

    @property
    def root(self):
        ''' get root command '''
        if self.parent is None:
            return self
        return self.parent.root

    @property
    def name(self):
        ''' Get name of the command '''
        return self.command.name

    @property
    def path(self):
        ''' Generate Path '''
        return self.delimited_path(delimiter="_")

    def delimited_path(self, delimiter="_"):
        ''' Generate Path Using a delimiter '''
        path = self.list_path()
        return delimiter.join(path)

    def list_path(self):
        ''' Generate Path as a list, starting with top-most sub item '''
        path = []
        name = self.name
        if self.parent:
            path = self.parent.list_path()
        if name:
            path.append(name)
        return path

    @property
    def dest(self):
        ''' Get Destination key for arguments for this command '''
        if self.command.actions_dest:
            return self.command.actions_dest
        path = self.path

        if not path:
            return self.command.actions_dest_base
        return "%s_%s" % (path, self.command.actions_dest_base)

    def parser_args(self, parser):
        ''' Add arguments to parser '''
        return self.command.parser_args(parser)

    def configure_parser(self, parser):
        ''' Configure Parser '''
        parser = self.parser_args(parser)
        if self.has_actions:
            subparsers = parser.add_subparsers(dest=self.dest,
                                               help=self.command.actions_desc,
                                               title=self.command.actions_title,
                                               metavar=self.command.actions_metavar)

            for action in self.actions:
                args = {'help': action.desc}
                if action.aliases and not IS_PYTHON2:
                    args['aliases'] = action.aliases
                subparser = subparsers.add_parser(action.name, **args)
                action.configure_parser(subparser)

        return parser

    def execute(self, args, wrapper=None):
        ''' Execute Command '''
        self.command.prep_command(args, self)
        if self.has_actions:
            action_name = args.get(self.dest, None)
            if action_name is not None:
                action = self.actions_idx.get(action_name)
                if action:
                    return action.execute(args, self)
                else:
                    return self.command.on_invalid_action(action_name, self)
            else:
                return self.command.on_missing_action(self)
        return self.command.execute(args, self)

    def __getattr__(self, name):
        ''' Get attribute '''
        return getattr(self.command, name)
