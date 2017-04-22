from __future__ import (absolute_import, division, print_function)

import json
import logging


class Logger(object):
    def __init__(self, name):
        self._logger = logging.getLogger(name)

    def debug(self, args):
        self._logger.debug(json.dumps(args))

    def info(self, args):
        self._logger.info(json.dumps(args))

    def warning(self, args):
        self._logger.warning(json.dumps(args))

    def error(self, args):
        self._logger.error(json.dumps(args))
