import pytest

from playbook.actions import ActionExecutor
from playbook.errors import UnknownAction


def test_action_command_instance():
    assert isinstance(ActionExecutor('shell'), ActionExecutor)


def test_action_command_apply_simple_cmd():
    args = ['echo', 'Test playbook']
    action = ActionExecutor('shell', *args)
    assert action.name == 'playbook.actions.basic.shell'

    for r in action.apply({}):
        assert r.get(u'status') == u'SUCCESS'
        assert r.get(u'exitcode') == 0
        assert r.get(u'stdout') == u'Test playbook\n'
        assert r.get(u'stderr') == u''
        assert r.get(u'msg') == u''


def test_action_command_apply_simple_cmd_with_error():
    args = ['echo', 'Test playbook']
    with pytest.raises(UnknownAction):
        assert ActionExecutor('shel', *args)
