# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

from ardy.core.triggers.driver import Trigger
from ardy.utils.log import logger


class Driver(Trigger):
    _DEPLOY_KEYS_WHITELIST = ["Id", "LambdaFunctionArn", "Events", "Filter"]

    _LAMBDA_ARN_KEY = "LambdaFunctionArn"

    get_awsservice_method = "get_s3_resource"

    trigget_type = "s3"

    def put(self, *args, **kwargs):
        triggers_conf = self.get_triggers()
        for trigger_conf in triggers_conf:
            logger.info("START to deploy S3 triggers for bucket {}".format(trigger_conf['bucket_name']))

            bucket_notification = self.client.BucketNotification(trigger_conf['bucket_name'])

            StatementId = "{}-{}".format(self.lambda_conf["FunctionName"], trigger_conf['bucket_name'])
            if not self.lambda_exist_policy(self.lambda_conf["FunctionName"], StatementId):
                self.awslambda.add_permission(
                    Action='lambda:InvokeFunction',
                    FunctionName=self.lambda_function_arn,
                    Principal='s3.amazonaws.com',
                    StatementId=StatementId
                )
            bucket_notification.put(
                NotificationConfiguration={'LambdaFunctionConfigurations': [self.get_deploy_conf(trigger_conf), ]}
            )
