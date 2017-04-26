import pytest

from playbook.tasks import Task
from playbook.errors import UnknownAction


def test_tasks_create():
    with pytest.raises(UnknownAction):
        assert Task()

    task = Task(name="Test task", shell='echo "Hello"')
    assert task.name == 'Test task'
    assert task.action == 'shell'

def test_tasks_execute():

    task = Task(name="Test task", shell='echo "Hello"')
    assert task.execute() == {
        u'exitcode': 0,
        u'msg': u'',
        u'status': u'SUCCESS',
        u'stderr': u'',
        u'stdout': u'Hello\n'
    }

def test_tasks_parse_args():

    assert Task(name="Test", shell='echo "Hello"')._parse_args() == (['echo', 'Hello'], {})
    assert Task(name="Test", shell='echo "Hello world"')._parse_args() == (['echo', 'Hello world'], {})
    assert Task(name="Test", shell='ls -l /tmp')._parse_args() == (['ls', '-l', '/tmp'], {})
    assert Task(name="Test", shell="name=httpd state=latest")._parse_args() == ([], {'name': 'httpd', 'state':'latest'})
    assert Task(name="Test", shell="verbose name=httpd state=latest")._parse_args() == (['verbose'],{'name': 'httpd', 'state':'latest'})
