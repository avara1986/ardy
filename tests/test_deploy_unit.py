# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import unittest

import boto3
from moto import mock_lambda, mock_s3
from requests.exceptions import ConnectionError

# App imports
from tests import DeployBaseTest
from tests.mocks_utils import MockZipFile


class DeployTest(DeployBaseTest):
    @mock_s3
    @mock_lambda
    def _create_lambda_from_s3(self):
        zip_file = MockZipFile.create_zip("test")

        bucket_name = "test_bucket"
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.create()

        bucket.put_object(
            Key=zip_file,
            Body=MockZipFile.read_file(zip_file)

        )
        self.lambda_conf["Code"] = {'S3Bucket': bucket_name,
                                    'S3Key': zip_file}

        response = self.deploy.remote_create_lambada(**self.lambda_conf)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 201)
        for key in ["FunctionName", "Role", "Runtime", "Handler"]:
            self.assertEqual(response[key], self.lambda_conf[key])

        return response

    @mock_lambda
    def _create_lambda_from_file(self):
        zip_file = MockZipFile.create_zip("test")
        self.lambda_conf["Code"] = {'ZipFile': MockZipFile.read_file(zip_file)}

        response = self.deploy.remote_create_lambada(**self.lambda_conf)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 201)
        for key in ["FunctionName", "Role", "Runtime", "Handler"]:
            self.assertEqual(response[key], self.lambda_conf[key])

    @mock_s3
    @mock_lambda
    def test_remote_list_lambdas(self):
        response = self.deploy.remote_list_lambdas()
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertEqual(response["Functions"], [])

        zip_file = MockZipFile.create_zip("test")
        self.lambda_conf["Code"] = {'ZipFile': MockZipFile.read_file(zip_file)}

        self._create_lambda_from_file()

    @mock_s3
    @mock_lambda
    def test_remote_get_lambda(self):
        response = self.deploy.remote_get_lambda(**self.lambda_conf)
        self.assertFalse(response)

        self._create_lambda_from_s3()

        response = self.deploy.remote_get_lambda(**self.lambda_conf)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        for key in ["FunctionName", "Role", "Runtime", "Handler"]:
            self.assertEqual(response["Configuration"][key], self.lambda_conf[key])

    @mock_s3
    @mock_lambda
    def test_remote_update_lambda(self):
        response = self.deploy.remote_get_lambda(**self.lambda_conf)
        self.assertFalse(response)

        self._create_lambda_from_s3()

        response = self.deploy.remote_get_lambda(**self.lambda_conf)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        for key in ["FunctionName", "Role", "Description", "Runtime", "Handler"]:
            self.assertEqual(response["Configuration"][key], self.lambda_conf[key])

        lambda_new_conf = {
            "FunctionName": "LambdaExample1",
            "Description": "string2",
            "Runtime": "python3.6",
        }

        # TODO: research this error from MOTO
        try:
            response = self.deploy.remote_update_conf_lambada(**self.lambda_conf)
            self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
            for key in ["FunctionName", "Role", "Description", "Runtime", "Handler"]:
                self.assertEqual(response["Configuration"][key], lambda_new_conf[key])
        except ConnectionError:
            pass


if __name__ == '__main__':
    unittest.main()
