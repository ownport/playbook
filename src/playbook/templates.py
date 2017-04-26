from __future__ import (absolute_import, division, print_function)

import logging

from six import string_types

from jinja2 import Environment
from jinja2.runtime import StrictUndefined
from jinja2.exceptions import TemplateSyntaxError, UndefinedError

from playbook.errors import TemplatesError

DEFAULT_JINJA2_EXTENSIONS = None

logger = logging.getLogger(__name__)


def get_extensions():
    ''' Return jinja2 extensions to load.
    '''

    jinja_exts = []
    if DEFAULT_JINJA2_EXTENSIONS:
        # make sure the configuration directive doesn't contain spaces
        # and split extensions in an array
        jinja_exts = DEFAULT_JINJA2_EXTENSIONS.replace(" ", "").split(',')

    return jinja_exts


def finalize(thing):
    ''' A custom finalize method for jinja2, which prevents None from being returned
    '''
    return thing if thing is not None else ''


class Template(object):
    def __init__(self, filters=None, tests=None):

        self._env = Environment(
            trim_blocks=True,
            undefined=StrictUndefined,
            extensions=get_extensions(),
            finalize=finalize)

        if isinstance(filters, dict):
            self._env.filters.update(filters)

        if isinstance(tests, dict):
            self._env.tests.update(tests)

    def render(self, data, vars):

        if not data:
            return data

        if isinstance(data, string_types):
            return self._do_render(data, vars)

        if isinstance(data, (list, tuple)):
            return [self.render(e, vars) for e in data]

        if isinstance(data, dict):
            return dict([(k, self.render(v, vars)) for k, v in data.items()])

        return data

    def _do_render(self, data, vars):
        ''' render data (template) with vars 
        
        :param data, the template string
        :param vars, the dictionery with variables
        
        :return data string after J2 templates rendering
        '''

        env = self._env.overlay()
        try:
            t = env.from_string(data)
        except TemplateSyntaxError as e:
            raise TemplatesError("template error while templating string: %s. String: %s" % (str(e), str(data)))
        except Exception as e:
            if 'recursion' in str(e):
                raise TemplatesError("recursive loop detected in template string: %s" % str(data))
            else:
                return data

        return t.render(**vars)
