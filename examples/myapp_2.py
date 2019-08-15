''' My Application '''

from quick_cli import Action
from quick_cli import QuickCLIApp
from quick_cli import QuickCLIAppLogged


__all__ = []
__version__ = '0.0.2'
__date__ = '2019-08-11'
__updated__ = '2019-08-14'


def one(args, wrapper):
    print("ONE! Running with args: %s" % args)


def two(args, wrapper):
    print("TWO! Running with args: %s" % args)


def three(args):
    print("Running with args: %s" % args)


def make_test_action(msg):
    def action(arg, wrapper):
        print("MSG: %s" % msg)
    return action


CONFIG_FLAG = [dict(flags='-c', dest='config', help="Config file")]


class MyApp(QuickCLIAppLogged):
    ''' My Sample App '''
    DEBUG = True

    ACTIONS = [
        Action("one", aliases=['1', 'o'], action=one, actions_desc="Second Tier Actions",
               args=[
                   CONFIG_FLAG,
                   dict(flags='--test', dest="test",
                        action="store_true", help="test flag")
        ],
            actions=[
                   Action('uno', action=make_test_action("uno")),
                   Action('dos', action=make_test_action("dos"))
        ]),
        Action("two", aliases=['2', 't'], action=two),
        Action("3", action=three)
    ]

    DESC = "Action One Description"

    program_epilog = '''
    
That is all that we can show right now

Have fun!

'''

    def prep_command(self, args, wrapper):
        ''' PreExecution Hook '''
        print("Pre-Ex in App!")

    def execute(self, args, wrapper):
        print("Verbosity: %s" % self.arg_value('verbosity', 'unset'))
        print("args: %s" % self.args)


if __name__ == "__main__":
    app = MyApp(init_logging=True, program_creator="M3",
                program_org="Legrig Universal")
    app.run()
