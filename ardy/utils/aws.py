# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

import boto3

from ardy.config import ConfigMixin


class AWSCli(ConfigMixin):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", False)
        if not self.config:
            super(AWSCli, self).__init__(*args, **kwargs)

    def _get_aws_cretentials_from_config(self):
        conf = {}
        aws_credentials = self.config.get("aws_credentials", {})
        aws_access_key_id = aws_credentials.get("aws_access_key_id", False)
        aws_secret_access_key = aws_credentials.get("aws_secret_access_key", False)
        region = aws_credentials.get("region", False)
        if aws_access_key_id:
            conf.update({"aws_access_key_id": aws_access_key_id})
        if aws_secret_access_key:
            conf.update({"aws_secret_access_key": aws_secret_access_key})
        if region:
            conf.update({"region_name": region})
        return conf

    def _get_client(self, client):
        return boto3.client(client, **self._get_aws_cretentials_from_config())

    def _get_resource(self, client):
        return boto3.resource(client, **self._get_aws_cretentials_from_config())

    def get_lambda_client(self):
        return self._get_client("lambda")

    def get_s3_resource(self):
        return self._get_resource("s3")

    def get_sns_client(self):
        return self._get_client("sns")

    def get_cloudwatchevent_client(self):
        return self._get_client("events")
