from __future__ import (absolute_import, division, print_function)

from plumbum import local
from plumbum.commands.processes import ProcessExecutionError


class Action(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def run(self):
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
