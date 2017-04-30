import pytest

from playbook.tasks import Task
from playbook.errors import UnknownAction


def test_tasks_create():
    with pytest.raises(UnknownAction):
        assert Task()

    task = Task(shell='echo "Hello"')
    assert task.action == 'shell'

def test_tasks_execute():

    task = Task(shell='echo "Hello"')
    for r in task.execute({}):
        assert r.get(u'exitcode') == 0
        assert r.get(u'msg') == u''
        assert r.get(u'status') == u'SUCCESS'
        assert r.get(u'stderr') == u''
        assert r.get(u'stdout') == u'Hello\n'


def test_tasks_parse_args():

    assert Task(shell='echo "Hello"')._parse_args() == (['echo', 'Hello'], {})
    assert Task(shell='echo "Hello world"')._parse_args() == (['echo', 'Hello world'], {})
    assert Task(shell='ls -l /tmp')._parse_args() == (['ls', '-l', '/tmp'], {})
    assert Task(shell="name=httpd state=latest")._parse_args() == ([], {'name': 'httpd', 'state':'latest'})
    assert Task(shell="verbose name=httpd state=latest")._parse_args() == (['verbose'],{'name': 'httpd', 'state':'latest'})
