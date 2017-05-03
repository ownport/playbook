from __future__ import (absolute_import, division, print_function)

from playbook.actions import BaseAction


class Action(BaseAction):

    name = 'foreach'

    def handler(self):
        return [r for r in self.next()]

    def next(self):
        for arg in self._args:
            yield {u'data': arg}

    def __iter__(self):
        return self.next()

