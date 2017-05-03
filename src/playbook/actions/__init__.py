from __future__ import (absolute_import, division, print_function)

import copy
import time

from playbook.templates import Template
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


class ActionResult(object):
    def __init__(self, action_name, action_descr='', invocation=None):
        self._result = {
            # initial
            u'action': action_name,
            u'description': action_descr,
            u'invocation': invocation,

            # execution time
            u'time.start': self._get_time(),
            u'time.end': None,
            u'time.delta': 0,

            # results variables
            u'status': None,
            u'rc': None,
            u'msg': None,
            u'data': None,
            u'stdout': None,
            u'stderr': None,
        }

    @staticmethod
    def _get_time():
        return time.time()

    def complete(self, status=None, exitcode=None, msg=None, data=None, stdout=None, stderr=None):
        self._result[u'time.end'] = self._get_time()
        self._result[u'time.delta'] = self._result[u'time.end'] - self._result[u'time.start']

        self._result[u'status'] = status
        self._result[u'exitcode'] = exitcode
        self._result[u'msg'] = msg
        self._result[u'data'] = data
        self._result[u'stdout'] = stdout
        self._result[u'stderr'] = stderr
        return self._result.copy()

    def __dict__(self):
        return self._result.copy()


class BaseAction(object):
    name = 'base.action'

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def handler(self):
        raise NotImplemented()

    def run(self):
        _invocation = {'args': self._args, 'kwargs': self._kwargs}
        result = ActionResult(action_name=self.name,
                              action_descr=self._kwargs.get('description', ''),
                              invocation=_invocation)
        _res = self.handler()
        if isinstance(_res, dict):
            return result.complete(**_res)
        elif isinstance(_res, (list, tuple)):
            return [result.complete(**item) for item in _res]


class ActionExecutor(object):
    def __init__(self, alias, *args, **kwargs):
        self._name = find_action(alias)
        if not self._name:
            raise UnknownAction('Unknown action, %s' % alias)

        self._action = self._import_action(self._name)

        self._args = args
        self._kwargs = kwargs

    @property
    def name(self):
        return self._name

    def _import_action(self, name):
        _module = __import__(name, globals(), locals(), ['Action'])
        return getattr(_module, 'Action')

    def apply(self, vars):
        template = Template()
        args = copy.deepcopy(self._args)
        kwargs = copy.deepcopy(self._kwargs)

        # pipeline: foreach -> when -> action
        processors = list()

        if 'foreach' in self._kwargs and self._kwargs.get('foreach', None):
            action = self._import_action(ACTIONS.get('foreach'))
            processors.append(action(*self._kwargs.pop('foreach')))

        if 'when' in self._kwargs and self._kwargs.get('when', None):
            action = self._import_action(ACTIONS.get('when'))
            processors.append(action(*self._kwargs.pop('when')))

        # processing logic
        for proc in processors:
            print(proc)

        # handling foreach action
        foreach_args = self._kwargs.get('foreach', None)
        if foreach_args:
            foreach_action = self._import_action(ACTIONS.get('foreach'))
            for item in foreach_action(*foreach_args).run():
                _vars = vars.copy()
                _vars[u'item'] = item[u'data']
                args = template.render(self._args, _vars)
                kwargs = template.render(self._kwargs, _vars)

        # conditions

        yield self._action(*args, **kwargs).run()


ACTIONS = {
    # basic
    'command': 'playbook.actions.basic.shell',
    'shell': 'playbook.actions.basic.shell',
    'script': 'playbook.actions.basic.script',

    # conditions
    'when': 'playbook.controls.conditions.case_when',

    # loops
    'foreach': 'playbook.controls.loops.foreach',
}
