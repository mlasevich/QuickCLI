''' QuickCLI Top Level Application '''
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import logging
import sys
import traceback

from quick_cli.subcmd_int import QuickCLICommandWrapper

from .app_info import QuickCLIAppBaseInfo
from .context import QuickCLIContext
from .subcmd import QuickCLISubCommand


LOG = logging.getLogger(__name__)


class QuickCLIApp(QuickCLIAppBaseInfo, QuickCLISubCommand):
    ''' QuickCLI Application Base '''
    DEBUG = False

    def __init__(self, **kwargs):
        ''' Constructor for QuickCLIApp Base '''
        context = kwargs.get('context', QuickCLIContext(self))
        if 'context' in kwargs:
            del kwargs['context']
        context.update(kwargs)
        self.context = context
        QuickCLIAppBaseInfo.__init__(self, **kwargs)
        QuickCLISubCommand.__init__(self, None)
        self.command = QuickCLICommandWrapper(self, None)

    def parser(self):
        ''' Create App Args Parser '''
        parser = ArgumentParser(description=self.info.program_desc,
                                prog=self.info.program_name,
                                epilog=self.info.program_epilog,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version',
                            action='version', version=self.info.program_version_message)
        return parser

    @property
    def args(self):
        ''' Get args from context '''
        return self.context.setdefault('args', {})

    def arg_value(self, arg, default_value=None):
        ''' Get Argument value by key, with default value '''
        return self.args.get(arg, default_value)

    def on_keyboard_interrupt(self):
        ''' Executed On Keyboard Interrupt '''
        LOG.debug("Keyboard Interrupt Called")
        return 0

    def _on_keyboard_interrupt(self):
        ''' Executed On Keyboard Interrupt (wrapper) '''
        LOG.debug("Keyboard Interrupt Called")
        return self.on_keyboard_interrupt()

    def on_error(self, exception):
        ''' Executed On Uncaught Exception - User overridable '''
        indent = len(self.info.program_name) * " "
        if self.DEBUG:
            traceback.print_exc()

        sys.stderr.write(self.info.program_name +
                         ": " + repr(exception) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

    def _on_error(self, exception):
        ''' Executed On Uncaught Exception (wrapper) '''
        LOG.info("Uncaught Exception: %s: %s",
                 exception.__class__.__name__, exception)
        self.on_error(exception)

    def pre_parser_config(self):
        ''' Hook for execution on before parser configuration '''

    def pre_parsing(self):
        ''' Hook for execution on before parsing arguments '''

    def post_parsing(self, args):
        ''' Hook for execution after parsing arguments '''

    def pre_execute(self):
        ''' Hook for execution after before main execution'''

    def _process_args(self, args):
        ''' Process Arguments '''
        self.context.set('args_ns', args)  # Do we need this?
        self.context.set('args', vars(args))
        self.process_args()

    def run(self, argv=None):
        ''' Run this CLI '''
        if argv is None:
            argv = sys.argv
        else:
            sys.argv.extend(argv)

        try:
            self.pre_parser_config()

            parser = self.parser()

            parser = self.command.configure_parser(parser)
            self.pre_parsing()
            args = parser.parse_args()
            self.post_parsing(args)

            self._process_args(args)

            self.pre_execute()
            return self.command.execute(self.args)

        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            return self._on_keyboard_interrupt()
        except Exception as ex:  # pylint: disable=broad-except
            return self._on_error(ex)


class QuickCLIAppLogged(QuickCLIApp):
    ''' QuickCLI Top Level Application Class, with Logging support '''

    DEBUG = False

    def __init__(self, **kwargs):
        ''' Constructor for QuickCLIApp '''
        QuickCLIApp.__init__(self, **kwargs)

    def parser(self):
        parser = super(QuickCLIAppLogged, self).parser()
        parser.add_argument('-v', '--verbose', action="count", dest="verbosity", default=0,
                            help="Increase verbosity level [default: %(default)s]")
        return parser

    def get_log_level(self):
        ''' Get Log Level '''
        verbosity = self.arg_value('verbosity', 0)
        if verbosity > 2:
            return logging.DEBUG
        if verbosity > 1:
            return logging.INFO
        return logging.WARNING

    def initialize_logging(self):
        ''' Initialize Logging '''
        loglevel = self.get_log_level()
        logging.basicConfig(level=loglevel)

    def pre_execute(self):
        ''' Hook for execution after parsing arguments '''
        if self.context.init_logging:
            self.initialize_logging()

    def execute(self, args, wrapper):
        ''' Main Section of execution '''
        LOG.info("Running application with args: %s", args)
        if self.command.has_subcommands:
            return self.command.execute(args)
        return 0
