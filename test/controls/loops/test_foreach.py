from playbook.controls.loops.foreach import Action


def test_actions_loops_foreach_create():
    foreach = Action()
    assert isinstance(foreach, Action)

def test_actions_loops_foreach_run():
    foreach = Action(*[1,2,3])
    assert [i[u'data'] for i in foreach.run()] == [1,2,3]
