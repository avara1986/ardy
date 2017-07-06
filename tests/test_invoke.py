# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os
import unittest

from ardy.core.invoke import Invoke

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))

class InvokeTest(unittest.TestCase):
    EXAMPLE_PROJECT = "myexamplelambdaproject"

    def setUp(self):
        pass

    def test_init(self):
        invoke = Invoke(path=TESTS_PATH)

        invoke.run("LambdaExample1")


if __name__ == '__main__':
    unittest.main()
