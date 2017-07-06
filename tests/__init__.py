# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os
import unittest

# App imports
from ardy.core.deploy import Deploy
from tests.mocks_utils import MockZipFile


class DeployBaseTest(unittest.TestCase):
    lambda_function_name = "LambdaExample1"
    lambda_conf = {
        "FunctionName": "LambdaExample1",
        "Handler": "myexamplelambdaproject.lambda1.main.my_handler",
        "Description": "string1",
        "Runtime": "python3.6",
        "Role": "example_role",
        "Code": {},
        "Tags": {},
    }

    def setUp(self):
        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)))
