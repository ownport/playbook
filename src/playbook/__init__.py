from __future__ import (absolute_import, division, print_function)

from playbook.log import Logger
from playbook.tasks import Task
from playbook.actions import find_action
from playbook.dataloader import DataLoader

PLAYBOOK_VERSION = '0.1.0'

logger = Logger(__name__)


class Playbook(object):
    def __init__(self, path, **args):

        self.path = path
        self.args = args

        self._tasks = []
        self._vars = {}

    def verify(self):
        self._parse()
        # print(self.vars)
        # print(self.tasks)

    @property
    def tasks(self):
        return self._tasks

    @property
    def vars(self):
        return self._vars

    def _parse(self):

        data = DataLoader().load_from_file(self.path)
        for play in data:
            if 'vars' in play and isinstance(play['vars'], dict):
                self._vars = play.get('vars')
            if 'tasks' in play and isinstance(play['tasks'], list):
                self._tasks = play.get('tasks')

    def run(self):
        ''' verify and run playbook 
        '''
        self.verify()

        # print(self.vars)

        for kwargs in self.tasks:
            task = Task(**kwargs)

            for result in task.execute(self._vars):
                if result['status'] == 'FAILED':
                    logger.error(dict(name=result['description'], msg=result['msg'], status=result['status']))
                    break
                else:
                    logger.info(dict(name=result['description'], status=result['status']))
                logger.debug(result)
