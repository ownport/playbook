from __future__ import (absolute_import, division, print_function)

from playbook.actions import BaseAction

from plumbum import local
from plumbum.commands.processes import ProcessExecutionError


class Action(BaseAction):

    name = u'shell'

    def handler(self):
        msg = ''
        try:
            exitcode, stdout, stderr = local.get(self._args[0]).run(self._args[1:])
        except ProcessExecutionError as err:
            exitcode = err.retcode
            stdout = err.stdout
            stderr = err.stderr
            msg = err.stderr

        return {
            'status': 'SUCCESS' if exitcode == 0 else 'FAILED',
            'exitcode': exitcode,
            'msg': msg,
            'stdout': stdout,
            'stderr': stderr
        }
