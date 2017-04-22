from __future__ import (absolute_import, division, print_function)

import sys
import json


def run_module_test(module, args):
    ''' run module test 
    '''

    class Stdin():

        def __init__(self, args):
            self._args = dict()
            if args and isinstance(args, list):
                self._args.update(dict([arg.split('=', 1) for arg in args]))

        def read(self):
            return json.dumps(dict(ANSIBLE_MODULE_ARGS=self._args))

    # TODO wrap stdin & stdout
    # from pprint import pprint

    sys.stdin = Stdin(args)
    try:
        module = __import__(
            'ansiblite.modules.{}'.format(module),
            globals(), locals(), ['main'])
        module.main()
    except ImportError as err:
        print("Cannot import module 'ansiblite.modules.{}'. Error: {}".format(module, err.message))

        import traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback)
        sys.exit(1)
    # print stdout.get()


def run_playbook(playbook, args):
    ''' run playbook
    '''
    from ansiblite.playbook import Playbook
    from ansiblite.executor.task_executor import TaskExecutor
    from ansiblite.parsing.dataloader import DataLoader

    _loader = DataLoader()
    for play in Playbook.load(playbook, loader=_loader).get_plays():
        for block in play.compile():
            for task in block.block:
                print(TaskExecutor(task, loader=_loader, job_vars={}).run())
