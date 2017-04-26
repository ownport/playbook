from __future__ import (absolute_import, division, print_function)

import pytest

from playbook.templates import Template
from playbook.errors import TemplatesError


def test_templates_instance():
    t = Template()
    assert isinstance(t, Template)


def test_templates_render_incorrect_template():
    assert Template().render('', {}) == ''
    assert Template().render(None, {}) == None

    with pytest.raises(TemplatesError):
        assert Template().render('{{', {}) == None


def test_templates__render():
    assert Template()._do_render('k1:{{v1}}', {'v1': '123'}) == 'k1:123'
    assert Template()._do_render('{{v1}},{{v1}},{{v1}}', {'v1': '#'}) == '#,#,#'
    assert Template()._do_render('{% for i in range(3) %}{{i}}{% endfor %}', {}) == '012'


def test_templates_render():
    # None or empty
    assert Template().render('', {'v1': '123'}) == ''
    assert Template().render(None, {'v1': '123'}) == None

    # string types
    assert Template().render('k1:{{v1}}', {'v1': '123'}) == 'k1:123'
    assert Template().render(u'k1:{{v1}}', {'v1': '123'}) == u'k1:123'

    # list or tuplese
    assert Template().render(['{{v}}1', '{{v}}2', '{{v}}3'], {'v': '#'}) == ['#1', '#2', '#3']

    # dict
    dict_sample = {'k1': '{{v}}1', 'k2': '{{v}}2', 'k3': '{{v}}3'}
    assert Template().render(dict_sample, {'v': '#'}) == {'k1': '#1', 'k2': '#2', 'k3': '#3'}

    # object
    assert isinstance(Template().render(Template(), {'v1': '123'}), Template)
