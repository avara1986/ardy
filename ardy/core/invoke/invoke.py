# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

import importlib
import os
import sys
import time

from ardy.config import ConfigMixin
from ardy.utils.log import logger
from tests.mocks_utils import MockContext


class Invoke(ConfigMixin):
    def __init__(self, *args, **kwargs):
        super(Invoke, self).__init__(*args, **kwargs)

    def run(self, lambda_name, local=True):
        lambda_config = self.config.get_lambda_by_name(lambda_name)
        if local:
            result = self._run_local_lambda(lambda_config)
        else:
            pass

    def _run_local_lambda(self, lambda_config):
        prev_folder = os.getcwd()
        os.chdir(self.config.get_projectdir())
        sys.path.append(self.config.get_projectdir())
        lambda_name = lambda_config["FunctionName"]
        lambda_handler = self.import_function(lambda_config["Handler"])

        # Run and set a counter
        start = time.time()
        results = lambda_handler({}, MockContext(lambda_name))
        end = time.time()

        # restore folder
        os.chdir(prev_folder)

        # Print results
        logger.info("{0}".format(results))
        logger.info("\nexecution time: {:.8f}s\nfunction execution "
                    "timeout: {:2}s".format(end - start, lambda_config["Timeout"]))

    def import_function(self, name):
        components = name.split('.')
        module = importlib.import_module(".".join(components[:-1]))
        return getattr(module, components[-1])
