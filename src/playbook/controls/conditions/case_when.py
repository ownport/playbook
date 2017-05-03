from __future__ import (absolute_import, division, print_function)

from playbook.actions import BaseAction

class Action(BaseAction):

    name = u'when'

    def handler(self):

        result = False
        for arg in self._args:
            if not eval(arg):
                break
        else:
            result = True

        return {
            'status': 'SUCCESS' if result else 'FAILED',
        }

    def __ror__(self, source):
        pass