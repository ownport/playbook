from __future__ import (absolute_import, division, print_function)

from collections import defaultdict


class Variables(object):
    def __init__(self):
        self._vars = defaultdict(dict)

    def get_vars(self, section):
        ''' get the k/v for the section
        
        :param section: section name 
        :return return the k/v for the section
        '''
        result = {}
        if section in self._vars:
            result = self._vars.get(section)
        return result

    def set_vars(self, section, k, v):
        ''' set the k/v for the specific action
        :param section: section name
        :param k: parameter key
        :param v: parameter value
        '''
        print(self._vars[section])
