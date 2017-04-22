from __future__ import (absolute_import, division, print_function)

from playbook.errors import UnknownAction


def find_action(name):
    ''' find action
    :param name: action name 
    :return action path for import
    '''
    return ACTIONS.get(name, None)


def get_all():
    ''' 
    :return: the list of all available actions
    '''
    return ACTIONS.keys()


class ActionExecutor(object):
    def __init__(self, alias, *args, **kwargs):
        self._name = find_action(alias)
        if not self._name:
            raise UnknownAction('Unknown action, %s' % alias)

        self._module = __import__(self._name, globals(), locals(), ['Action'])
        self._action = getattr(self._module, 'Action')

        self._args = args
        self._kwargs = kwargs

    @property
    def name(self):
        return self._name

    def apply(self):
        return self._action(*self._args, **self._kwargs).run()


ACTIONS = {
    # basic
    'command': 'playbook.actions.basic.shell',
    'shell': 'playbook.actions.basic.shell',
}
