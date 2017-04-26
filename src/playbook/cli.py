from __future__ import (absolute_import, division, print_function)

import sys
import logging
import argparse

from playbook import PLAYBOOK_VERSION
from playbook import Playbook
from playbook.log import Logger

PLAYBOOK_USAGE = '''playbook <command> [<args>]

The list of commands:
   test             playbook testing and validation
   run              run playbook
'''

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logger = Logger(__name__)


class CLI(object):
    def __init__(self):

        parser = argparse.ArgumentParser(usage=PLAYBOOK_USAGE)
        parser.add_argument('-v', '--version', action='version',
                            version='playbook-v{}'.format(PLAYBOOK_VERSION))
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command: %s' % args.command)
            sys.exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    @staticmethod
    def test():

        parser = argparse.ArgumentParser(usage=PLAYBOOK_USAGE, description='Playbook testing and validation')
        parser.add_argument('-p', '--playbook',
                            dest='playbook_path',
                            required=True,
                            help="the playbook to execute")
        parser.add_argument('-a', '--args',
                            dest='playbook_args',
                            action='append',
                            help="playbook arguments")
        parser.add_argument('--syntax-check', dest='syntax',
                            action='store_true',
                            help="perform a syntax check on the playbook, but do not execute it")
        args = parser.parse_args(sys.argv[2:])

        if not args.playbook_path:
            parser.print_help()
            sys.exit(1)

        pb = Playbook(path=args.playbook_path, args=args.playbook_args)
        pb.verify()

    @staticmethod
    def run():

        parser = argparse.ArgumentParser(usage=PLAYBOOK_USAGE, description='run playbook(-s)')
        parser.add_argument('-v', '--verbose', dest='verbosity', default=0,
                            action="count",
                            help="verbose mode (-vvv for more, -vvvv to playbook debugging)")
        parser.add_argument('-p', '--playbook',
                            dest='playbook_path',
                            required=True,
                            help="the path to playbook")
        parser.add_argument('-a', '--args',
                            dest='playbook_args',
                            action='append',
                            help="playbook arguments")
        parser.add_argument('--list-tasks', dest='tasks_list', action='store_true',
                            help="list all tasks in te playbook")
        parser.add_argument('-l', '--loglevel', dest='log_level',
                            default=logging.INFO,
                            help='logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL')

        args = parser.parse_args(sys.argv[2:])

        if not args.playbook_path:
            parser.print_help()
            sys.exit(1)

        logging.basicConfig(level=args.log_level, handler=NullHandler(),
                            format="%(asctime)s (%(name)s) [%(levelname)s] %(message)s")

        pb = Playbook(path=args.playbook_path, args=args.playbook_args)
        pb.run()
