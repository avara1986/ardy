# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os
import unittest

from ardy.config import GlobalConfig, LambdaConfig


class ConfigTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_config(self):
        config = GlobalConfig(path=os.path.dirname(os.path.abspath(__file__)))

        # Test global conf
        self.assertEqual(config.version, 1)
        self.assertEqual(config["version"], 1)
        self.assertEqual(type(config.VpcConfig), dict)
        self.assertEqual(type(config["VpcConfig"]), dict)
        self.assertEqual(type(config["VpcConfig"]["SecurityGroupIds"]), list)
        self.assertEqual(type(config["VpcConfig"]["SubnetIds"]), list)
        self.assertEqual(config.Role, "example_role")
        self.assertEqual(config["Role"], "example_role")
        self.assertEqual(config["Role"], "example_role")
        self.assertEqual(config.MemorySize, 512)
        self.assertEqual(config["MemorySize"], 512)

        self.assertEqual(type(config.get_globals()), dict)
        self.assertEqual(config.get_globals()["version"], 1)
        self.assertEqual(config.get_globals().get("lambdas", False), False)

        # Test lambda
        self.assertEqual(type(config["lambdas"]), list)
        for aws_lambda in config["lambdas"]:
            self.assertTrue(isinstance(aws_lambda, LambdaConfig))
        self.assertEqual([i["FunctionName"] for i in config.get_lambdas()],
                         ["LambdaExample{}".format(i) for i in range(1, 4)])

        # Test each lambda
        self.assertEqual(config["lambdas"][0]["MemorySize"], 512)
        self.assertEqual(config["lambdas"][0]["Role"], "example_role")

        self.assertEqual(config["lambdas"][0]["MemorySize"], 512)
        self.assertEqual(config["lambdas"][1]["Role"], "example_role2")

    def test_environment_config(self):
        for environment in ["dev", "pre", "pro"]:
            config = GlobalConfig(path=os.path.dirname(os.path.abspath(__file__)), environment=environment)
            for i in range(1, 4):
                lambda_name = "LambdaExample{}".format(i)
                if i == 3:
                    lambda_name = "LambdaExample{}_{}".format(i, environment)

                self.assertEqual(config["lambdas"][i - 1]["FunctionName"], lambda_name)


if __name__ == '__main__':
    unittest.main()
