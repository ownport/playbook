from playbook.controls.conditions.case_when import Action

def test_actions_conditions_when():

    cond_when = Action(*['10 == 10'])
    assert isinstance(cond_when, Action)

def test_actions_conditions_when_run():

    assert Action(*['True']).run().get(u'action') == 'when'
    assert Action(*['False']).run().get(u'status') == 'FAILED'

    assert Action().run().get(u'status') == 'SUCCESS'

    assert Action(*['10 == 10']).run().get(u'status') == 'SUCCESS'
    assert Action(*['3 > 2', '2 > 1', '1 > 0']).run().get(u'status') == 'SUCCESS'

    assert Action(*['True', 'False']).run().get(u'status') == 'FAILED'
    assert Action(*['2 > 1', '1 > 2']).run().get(u'status') == 'FAILED'
