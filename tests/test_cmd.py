# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os
import shutil
import unittest
import sys
from mock import patch

from ardy.core.cmd import Command
from ardy.core.deploy import Deploy
from ardy.core.build import Build
from ardy.core.exceptions import ArdyNoDirError, ArdyNoFileError
from tests.utils import mkdir

TESTS_PATH = os.path.dirname(os.path.abspath(__file__))


class CmdTest(unittest.TestCase):
    deploy_environments = [
        "dev",
        "pre",
        "pro"
    ]
    base_arguments = arguments = ["-p", os.path.join(TESTS_PATH, "myexamplelambdaproject"), "-f",
                                  "myexamplelambdaproject_config.json"]



    def setUp(self):
        pass

    def assert_base_conf(self, command):
        self.assertEqual(command.args.project, os.path.join(TESTS_PATH, "myexamplelambdaproject"))
        self.assertEqual(command.args.conffile, "myexamplelambdaproject_config.json")

    def test_base(self):
        test_folder = "myexamplelambdaproject_test"
        try:
            arguments = ["-p", test_folder, "-f", "config.json"]
            Command(arguments=arguments, exit_at_finish=False)
            self.fail("notexist folder not exists")
        except ArdyNoDirError:
            pass

        mkdir(test_folder)

        try:
            arguments = ["-p", test_folder, "-f", "config.json"]
            Command(arguments=arguments, exit_at_finish=False)
            self.fail("config.json not exist in myexamplelambdaproject")
        except ArdyNoFileError:
            pass

        shutil.rmtree(test_folder)

        if sys.version_info <= (3, 0):
            with self.assertRaises(SystemExit):
                Command(arguments=self.base_arguments, exit_at_finish=False)
        else:
            command = Command(arguments=self.base_arguments, exit_at_finish=False)
            self.assert_base_conf(command)

    def test_deploy_error(self):
        lambda_functions_to_deploy = ["lambda1", "lambda2"]
        with self.assertRaises(SystemExit):
            Command(arguments=self.base_arguments + ["deploy", ] + lambda_functions_to_deploy, exit_at_finish=False)
            self.fail("Environment is needed is it's defined in config.json")

    @patch.object(Deploy, "run")
    def test_deploy(self, deploy_run_mock):
        lambda_functions_to_deploy = ["lambda1", "lambda2"]
        for environment in self.deploy_environments:
            arguments = self.base_arguments + ["deploy", ] + lambda_functions_to_deploy + [environment, ]
            deploy = Command(arguments=arguments, exit_at_finish=False)
            self.assertEqual(deploy.args.lambdafunctions, lambda_functions_to_deploy)
            self.assertEqual(deploy.args.environment, environment)

        self.assertEqual(deploy_run_mock.call_count, len(self.deploy_environments))
        self.assert_base_conf(deploy)

    @patch.object(Build, "run")
    def test_build(self, build_run_mock):
        arguments = self.base_arguments + ["build", ]
        build = Command(arguments=arguments, exit_at_finish=False)
        self.assertEqual(build_run_mock.call_count, 1)
        self.assert_base_conf(build)

if __name__ == '__main__':
    unittest.main()
