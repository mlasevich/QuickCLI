''' My Application '''

from quick_cli import Action
from quick_cli import QuickCLIApp
from quick_cli import QuickCLIAppLogged


__all__ = []
__version__ = '0.0.2'
__date__ = '2019-08-11'
__updated__ = '2019-08-13'


class ActionOne(Action):
    ''' Action One '''
    ACTIONS_DESC = "as one"
    ACTIONS_TITLE = "title"

    DESC = "Action One Description"

    def parser_args(self, parser):
        ''' Add args '''
        parser.add_argument('-c', dest='config', help="Config file")
        return parser

    def prep_command(self, args, wrapper):
        ''' PreExecution Hook '''
        print("Pre-Ex %s!" % self.__class__.__name__)


class ActionThree(Action):
    ''' Action Three '''
    ACTIONS = [
        ActionOne('two', aliases=['wan']),
    ]

    def parser_args(self, parser):
        ''' Add args '''
        parser.add_argument('-c', dest='config', help="Config file")
        return parser

    def prep_command(self, args, wrapper):
        ''' PreExecution Hook '''
        print("Pre-Ex %s!" % self.__class__.__name__)


class ActionTwo(Action):
    '''
    Action Two!!

    This is my action
    '''
    ACTIONS = [
        ActionThree('two', aliases=['wan']),
        ActionOne('3')
    ]
    ACTIONS_DEST_BASE = "sub"

    def prep_command(self, args, wrapper):
        ''' PreExecution Hook '''
        print("Pre-Ex %s!" % self.__class__.__name__)


def run(args):
    print("Running with args: %s" % args)


class MyApp(QuickCLIAppLogged):
    ''' My Sample App '''
    DEBUG = True

    ACTIONS = [
        ActionOne("one", aliases=['1', 'o']),
        ActionTwo("two", aliases=['2', 't']),
        Action("3", action=run)
    ]
    ACTIONS_DESC = "as one"
    ACTIONS_TITLE = "title"

    DESC = "Action One Description"

    program_epilog = '''
    
That is all that we can show right now

Have fun!

'''

    def prep_command(self, args, wrapper):
        ''' PreExecution Hook '''
        print("Pre-Ex!")

    def execute(self, args, wrapper):
        print("Verbosity: %s" % self.arg_value('verbosity', 'unset'))
        print("args: %s" % self.args)


if __name__ == "__main__":
    app = MyApp(init_logging=True, program_creator="M3",
                program_org="Legrig Universal")
    app.run()
