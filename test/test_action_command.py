import pytest

from playbook.actions import ActionExecutor
from playbook.errors import UnknownAction

def test_action_command_instance():
    assert isinstance(ActionExecutor('shell'), ActionExecutor)


def test_action_command_apply_simple_cmd():
    args = ['echo', 'Test playbook']
    action = ActionExecutor('shell', *args)
    assert action.name == 'playbook.actions.basic.shell'
    assert action.apply() == {
        'status': 'SUCCESS',
        'exitcode': 0,
        'stdout': 'Test playbook\n',
        'stderr': '',
        'msg': ''
    }

def test_action_command_apply_simple_cmd_with_error():
    args = ['echo', 'Test playbook']
    with pytest.raises(UnknownAction):
        assert ActionExecutor('shel', *args)
