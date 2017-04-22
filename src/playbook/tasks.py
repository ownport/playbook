from __future__ import (absolute_import, division, print_function)

from playbook import actions
from playbook.log import Logger
from playbook.errors import UnknownAction, IncorrectTaskArgsType

logger = Logger(__name__)


class Task(object):
    def __init__(self, **kwargs):

        if not isinstance(kwargs, dict):
            raise IncorrectTaskArgsType('Expected dict, %s' % type(kwargs))

        self._name = kwargs.pop('name', None)
        self._action = self._get_action_name(kwargs)
        if not self._action:
            raise UnknownAction('Unknown task action, %s' % kwargs)

        self._kwargs = kwargs

    @property
    def name(self):
        return self._name

    @property
    def action(self):
        return self._action

    def _get_action_name(self, kwargs):
        ''' returns action name if founded
        '''
        action = [k for k in kwargs.keys() if k in actions.get_all()]
        return action[0]

    def execute(self):
        ''' Execute the task '''
        args = self._kwargs.pop(self.action, '').split(' ')
        return actions.ActionExecutor(self._action, *args, **self._kwargs).apply()
