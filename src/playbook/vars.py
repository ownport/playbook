from __future__ import (absolute_import, division, print_function)

from collections import defaultdict


class Variables(object):
    def __init__(self):
        self._vars = defaultdict(dict)

    def put(self, section, kwargs):
        ''' set the k/v for the specific action
        :param section: section name
        :param kwargs: key/value pairs
        '''
        if isinstance(kwargs, dict):
            self._vars[section].update(kwargs)
        else:
            raise RuntimeError('Expected dict, found %s' % type(type(kwargs)))
        return self

    def get(self, section, k=None):
        ''' get the k/v for the section
        
        :param section: section name 
        :return the k/v for the section
        '''
        result = {}
        if section in self._vars:
            result = self._vars.get(section)
        result = result.get(k) if k else result
        return result

    @property
    def sections(self):
        return self._vars.keys()

    def all(self):
        ''' get all k/v
        :return all k/v variables
        '''
        return self._vars.items()
