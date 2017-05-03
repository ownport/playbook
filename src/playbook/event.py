from __future__ import (absolute_import, division, print_function)


class Event(object):
    def __init__(self, **kwargs):
        self._headers = kwargs.get(u'headers', dict())
        self._payload = kwargs.get(u'payload', None)

    @property
    def headers(self):
        return self._headers

    @property
    def payload(self):
        return self._payload

    def to_dict(self):
        return {
            u'headers': self.headers,
            u'payload': self.payload
        }
