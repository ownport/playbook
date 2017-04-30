from __future__ import (absolute_import, division, print_function)

from playbook.actions import BaseAction


class Action(BaseAction):

    name = 'foreach'

    def handler(self):
        _result = list()
        for arg in self._args:
            _result.append({u'data': arg})
        return _result
