from __future__ import (absolute_import, division, print_function)

from playbook.event import Event


def test_event_instance():
    event = Event()
    assert isinstance(event, Event)


def test_event_headers():
    event = Event(headers={'k1': 'v1', 'k2': 'v2'})
    assert event.headers == {'k1': 'v1', 'k2': 'v2'}


def test_event_payload():
    event = Event(payload='value')
    assert event.payload == 'value'


def test_event_headers_payload():
    event = Event(headers={'k1': 'v1', 'k2': 'v2'}, payload='value')
    assert event.headers == {'k1': 'v1', 'k2': 'v2'}
    assert event.payload == 'value'


def test_event_to_dict():
    event = Event(headers={'k1': 'v1', 'k2': 'v2'}, payload='value')
    assert event.to_dict() == {
        'headers': {'k1': 'v1', 'k2': 'v2'},
        'payload': 'value'
    }
