from __future__ import (absolute_import, division, print_function)

import shlex

from plumbum import local
from plumbum.commands.processes import ProcessExecutionError

from playbook.actions import BaseAction


class Action(BaseAction):
    name = u'script'

    def handler(self):
        for cmd in self._args:
            args = shlex.split(cmd)
            try:
                local.get(args[0]).run(args[1:])
            except ProcessExecutionError as err:
                return {
                    u'status': 'FAILED',
                    u'exitcode': err.retcode,
                    u'msg': err.stderr,
                    u'stdout': err.stdout,
                    u'stderr': err.stderr,
                }
        return {
            u'status': 'SUCCESS',
            u'exitcode': 0,
            u'msg': None,
            u'stdout': None,
            u'stderr': None
        }
