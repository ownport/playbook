from __future__ import (absolute_import, division, print_function)

import shlex

from six import string_types

from playbook import actions
from playbook.log import Logger
from playbook.errors import UnknownAction

logger = Logger(__name__)


class Task(object):
    def __init__(self, **kwargs):
        descr = kwargs.pop('name', '')
        if descr:
            kwargs['description'] = descr

        self._action = self._get_action_name(kwargs)
        if not self._action:
            raise UnknownAction('Unknown task action, %s' % kwargs)

        self._kwargs = kwargs

    @property
    def action(self):
        return self._action

    def _get_action_name(self, kwargs):
        ''' returns action name if founded
        '''
        if not kwargs:
            return None
        else:
            action = [k for k in kwargs.keys() if k in actions.get_all()]
            if action:
                return action[0]
            return None

    def _parse_args(self):
        ''' parse action arguments '''
        args = list()
        kwargs = self._kwargs.copy()
        action_args = kwargs.pop(self.action, '')
        if isinstance(action_args, string_types):
            for arg in shlex.split(action_args):
                kv = arg.split('=', 1)
                if len(kv) == 1:
                    args.append(kv[0])
                else:
                    kwargs.update({kv[0]: kv[1]})
        elif isinstance(action_args, (list, tuple)):
            args.extend(action_args)
        return (args, kwargs)

    def execute(self, vars):
        ''' Execute the task '''
        args, kwargs = self._parse_args()
        for res in actions.ActionExecutor(self._action, *args, **kwargs).apply(vars):
            yield res
