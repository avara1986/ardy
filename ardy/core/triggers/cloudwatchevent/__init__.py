# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

import json

from ardy.core.triggers.driver import Trigger
from ardy.utils.log import logger


class Driver(Trigger):
    _DEPLOY_KEYS_WHITELIST = ["Name", "ScheduleExpression", "EventPattern", "State", "Description", "RoleArn"]

    _LAMBDA_ARN_KEY = "LambdaFunctionArn"

    get_awsservice_method = "get_cloudwatchevent_client"

    trigget_type = "cloudwatchevent"

    def put(self, *args, **kwargs):
        triggers_conf = self.get_triggers()
        for trigger_conf in triggers_conf:
            rule_conf = self.get_deploy_conf(trigger_conf)
            logger.info("START to deploy CloudWatch Event triggers for rule {} with conf: {}".format(
                trigger_conf['Name'], json.dumps(rule_conf, indent=4, sort_keys=True))
            )
            self.client.put_rule(**self.get_deploy_conf(trigger_conf))

            StatementId = "{}-{}".format(self.lambda_conf["FunctionName"], trigger_conf['Name'])
            if not self.lambda_exist_policy(self.lambda_conf["FunctionName"], StatementId):
                self.awslambda.add_permission(
                    Action='lambda:InvokeFunction',
                    FunctionName=self.lambda_function_arn,
                    Principal='events.amazonaws.com',
                    StatementId=StatementId
                )

            target_conf = {
                'Id': self.lambda_conf["FunctionName"],
                'Arn': self.lambda_function_arn,
                'Input': trigger_conf.get("Input", ""),
            }
            logger.info("Put target CloudWatch {} with conf: {}".format(trigger_conf['Name'],
                                                                        json.dumps(target_conf, indent=4,
                                                                                   sort_keys=True)))
            self.client.put_targets(
                Rule=trigger_conf['Name'],
                Targets=[target_conf, ]
            )
