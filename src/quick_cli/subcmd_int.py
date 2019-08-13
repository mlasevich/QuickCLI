''' 
Subcommand Internal tools
'''
import logging
import sys

LOG = logging.getLogger(__name__)

IS_PYTHON2 = sys.version_info[0] == 2


class QuickCLICommandWrapper(object):

    def __init__(self, command, parent):
        ''' Constructor for Command Wrapper '''
        self.command = command
        self.parent = parent
        self.app = self.root.command

        self.sub_commands = []
        self.sub_cmd_idx = {}
        self._process_subcommands(command.SUBCOMMANDS)

    def _process_subcommands(self, subcommands):
        ''' Process subcommands '''
        for subcommand in subcommands:
            wrapped = QuickCLICommandWrapper(subcommand, self)
            self.sub_commands.append(wrapped)
            self.sub_cmd_idx[subcommand.name] = wrapped
        for wrapped in self.sub_commands:
            for alias in wrapped.aliases:
                if not alias in self.sub_cmd_idx:
                    self.sub_cmd_idx[alias] = wrapped

    @property
    def has_subcommands(self):
        ''' Check if we have sub-commands '''
        return True if self.sub_commands else False

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
        ''' Get Destination key for argumenrs for this command '''
        if self.command.SUBCOMMAND_DEST:
            return self.command.SUBCOMMAND_DEST
        path = self.path

        if not path:
            return self.command.SUBCOMMAND_DEST_BASE
        return "%s_%s" % (path, self.command.SUBCOMMAND_DEST_BASE)

    def parser_args(self, parser):
        ''' Add arguments to parser '''
        return self.command.parser_args(parser)

    def configure_parser(self, parser):
        ''' Configure Parser '''
        parser = self.parser_args(parser)
        if self.has_subcommands:
            subparsers = parser.add_subparsers(dest=self.dest,
                                               help=self.command.SUBCOMMAND_DESC,
                                               title=self.command.SUBCOMMAND_TITLE,
                                               metavar=self.command.SUBCOMMAND_META)

            for subcommand in self.sub_commands:
                args = {'help': subcommand.desc}
                if subcommand.aliases and not IS_PYTHON2:
                    args['aliases'] = subcommand.aliases
                subparser = subparsers.add_parser(subcommand.name, **args)
                subcommand.configure_parser(subparser)

        return parser

    def execute(self, args):
        ''' Execute Command '''
        self.command.prep_command(args, self)
        if self.has_subcommands:
            action_name = args.get(self.dest, None)
            if action_name is not None:
                subcommand = self.sub_cmd_idx.get(action_name)
                if subcommand:
                    return subcommand.execute(args)
                else:
                    return self.command.on_invalid_subcommand(action_name, self)
            else:
                return self.command.on_missing_subcommand(self)
        return self.command.execute(args)

    def __getattr__(self, name):
        ''' Get attribute '''
        return getattr(self.command, name)
