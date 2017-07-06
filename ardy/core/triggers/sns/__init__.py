# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

from ardy.core.triggers.driver import Trigger
from ardy.utils.log import logger


class Driver(Trigger):
    get_awsservice_method = "get_sns_client"

    trigget_type = "sns"

    def put(self, *args, **kwargs):
        triggers_conf = self.get_triggers()
        for trigger_conf in triggers_conf:
            logger.info("START to deploy SNS triggers for toppic {}".format(trigger_conf["TopicArn"]))
            self.client.subscribe(
                TopicArn=trigger_conf["TopicArn"],
                Protocol='lambda',
                Endpoint=self.lambda_function_arn
            )
            StatementId = "{}-{}".format(self.lambda_conf["FunctionName"], trigger_conf['TopicArn'].split(":")[-1])
            if not self.lambda_exist_policy(self.lambda_conf["FunctionName"], StatementId):
                self.awslambda.add_permission(
                    Action='lambda:InvokeFunction',
                    FunctionName=self.lambda_function_arn,
                    Principal='sns.amazonaws.com',
                    # SourceArn='arn:aws:s3:::{}/*'.format(trigger_conf['bucket_name']),
                    StatementId=StatementId
                )
