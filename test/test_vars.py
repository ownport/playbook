from __future__ import (absolute_import, division, print_function)

import pytest

from playbook.vars import Variables
from playbook.errors import PlaybookError


def test_vars_isinstance():
    assert isinstance(Variables(), Variables)


def test_vars_put_vars():
    _vars = Variables()
    _vars.put('s1', {'k1': 'v1'})
    assert _vars.all() == [('s1', {'k1':'v1'})]
    assert _vars.get('s1', 'k1') == 'v1'


def test_vars_put_vars_incorrect_kv_type():
    _vars = Variables()
    with pytest.raises(RuntimeError):
        _vars.put('s1', ('k1', 'v1'))


def test_vars_get_vars():
    _vars = Variables()
    _vars.put('s1', {'k1': 'v1', 'k2': 'v2'})
    assert _vars.get('s1') == {'k1': 'v1', 'k2': 'v2'}
    assert _vars.get('s1', 'k1') == 'v1'
    assert _vars.get('s1', 'k3') is None


def test_vars_sections_list():
    _vars = Variables().put('s1', {'k1': 'v1', 'k2': 'v2'})
    assert _vars.sections == ['s1', ]
