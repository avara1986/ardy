# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import os
import unittest

import boto3
import botocore
from mock import patch
from moto import mock_lambda, mock_s3, mock_sns, mock_cloudwatch
from requests.exceptions import ConnectionError

# App imports
from ardy.core.build.build import Build
from ardy.core.deploy import Deploy
from tests import DeployBaseTest
from tests.mocks_utils import MockZipFile

orig = botocore.client.BaseClient._make_api_call


def mock_make_api_call(self, operation_name, kwarg):
    if operation_name in ['PutRule',
                          'AddPermission',
                          'PutTargets',
                          'UpdateFunctionConfiguration',
                          'UpdateAlias',
                          'PutBucketNotificationConfiguration']:
        return {}
    elif operation_name in ["UpdateFunctionCode"]:
        return {"FunctionArn": "mylambda_arn"}
    return orig(self, operation_name, kwarg)


class DeployTest(DeployBaseTest):
    @mock_s3
    @mock_lambda
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run(self, create_artefact_mock, copytree_mock, pip_install_mock):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file

        # Create lambdas
        self.deploy.run("myexamplelambdaproject")

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertTrue(create_artefact_mock.called)

        # Update lambdas
        # self.deploy.run("myexamplelambdaproject")

        os.remove(zip_file)

    @mock_s3
    @mock_lambda
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    @patch.object(Deploy, "is_client_result_ok")
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run_with_version(self, create_artefact_mock, copytree_mock, pip_install_mock, is_client_result_ok):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file
        is_client_result_ok.return_value = True

        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)),
                             filename="config_with_alias_and_version.json")

        # TODO: Search why moto rise errors
        try:
            # Create lambdas
            self.deploy.run("myexamplelambdaproject")

            self.assertTrue(pip_install_mock.called)
            self.assertTrue(copytree_mock.called)
            self.assertTrue(create_artefact_mock.called)

            # Update lambdas
            self.deploy.run("myexamplelambdaproject")

        except ConnectionError as e:
            print(e)

        os.remove(zip_file)

    @mock_s3
    @mock_lambda
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    @patch.object(Deploy, "is_client_result_ok")
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run_with_version(self, create_artefact_mock, copytree_mock, pip_install_mock, is_client_result_ok):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file
        is_client_result_ok.return_value = True

        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)), filename="config_with_version.json")

        # Create lambdas
        self.deploy.run("myexamplelambdaproject")

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertTrue(create_artefact_mock.called)

        # Update lambdas
        self.deploy.run("myexamplelambdaproject")

        os.remove(zip_file)

    @mock_s3
    @mock_lambda
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    @patch.object(Deploy, "is_client_result_ok")
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run_with_alias(self, create_artefact_mock, copytree_mock, pip_install_mock, is_client_result_ok):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file
        is_client_result_ok.return_value = True

        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)), filename="config_with_alias.json")

        # Create lambdas
        self.deploy.run("myexamplelambdaproject")

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertTrue(create_artefact_mock.called)

        # Update lambdas
        self.deploy.run("myexamplelambdaproject")

        os.remove(zip_file)

    @mock_s3
    @mock_lambda
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    @patch.object(Deploy, "is_client_result_ok")
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run_with_trigger_s3(self, create_artefact_mock, copytree_mock, pip_install_mock, is_client_result_ok):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file
        is_client_result_ok.return_value = True

        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)), filename="config_with_triggers.json",
                             lambdas_to_deploy=["LambdaExample_S3_7", ])

        # Create lambdas
        self.deploy.run("myexamplelambdaproject")

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertTrue(create_artefact_mock.called)

        # Update lambdas
        self.deploy.run("myexamplelambdaproject")

        os.remove(zip_file)

    @mock_s3
    @mock_sns
    @mock_lambda
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    @patch.object(Deploy, "is_client_result_ok")
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run_with_trigger_sns(self, create_artefact_mock, copytree_mock, pip_install_mock, is_client_result_ok):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file
        is_client_result_ok.return_value = True

        client = boto3.client('sns', region_name="eu-west-1")
        _ = client.create_topic(
            Name='TestLambdas'
        )

        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)), filename="config_with_triggers.json",
                             lambdas_to_deploy=["LambdaExample_SNS_8", ])

        # Create lambdas
        self.deploy.run("myexamplelambdaproject")

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertTrue(create_artefact_mock.called)

        # Update lambdas
        self.deploy.run("myexamplelambdaproject")

        os.remove(zip_file)

    @mock_s3
    @mock_cloudwatch
    @mock_lambda
    @patch('botocore.client.BaseClient._make_api_call', new=mock_make_api_call)
    @patch.object(Deploy, "is_client_result_ok")
    @patch.object(Build, "pip_install_to_target")
    @patch.object(Build, "copytree")
    @patch.object(Build, "create_artefact")
    def test_run_with_trigger_cloudwatch(self, create_artefact_mock, copytree_mock, pip_install_mock,
                                         is_client_result_ok):
        zip_file = MockZipFile.create_zip("test")
        create_artefact_mock.return_value = zip_file
        is_client_result_ok.return_value = True

        self.deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)), filename="config_with_triggers.json",
                             lambdas_to_deploy=["LambdaExample_CWE_9", ])

        # Create lambdas
        self.deploy.run("myexamplelambdaproject")

        self.assertTrue(pip_install_mock.called)
        self.assertTrue(copytree_mock.called)
        self.assertTrue(create_artefact_mock.called)

        # Update lambdas
        self.deploy.run("myexamplelambdaproject")

        os.remove(zip_file)


if __name__ == '__main__':
    unittest.main()
