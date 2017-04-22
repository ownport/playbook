from __future__ import (absolute_import, division, print_function)

import sys

class Cleaner():

    @staticmethod
    def syspath():
        result = []
        for p in sys.path:
            if p.endswith('site-packages'):
                continue
            if p.endswith('dist-packages'):
                continue
            if p.endswith('lib-old'):
                continue
            if p.endswith('lib-tk'):
                continue
            if p.endswith('gtk-2.0'):
                continue
            result.append(p)
        return result
