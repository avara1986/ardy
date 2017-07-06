Triggers
========

AWS Lambda support AWS services that you can configure as event sources:

* Amazon S3
* Amazon DynamoDB
* Amazon Kinesis Streams
* Amazon Simple Notification Service
* Amazon Simple Email Service
* Amazon Cognito
* AWS CloudFormation
* Amazon CloudWatch Logs
* Amazon CloudWatch Events
* AWS CodeCommit
* Scheduled Events (powered by Amazon CloudWatch Events)
* AWS Config
* Amazon Alexa
* Amazon Lex
* Amazon API Gateway
* Other Event Sources: Invoking a Lambda Function On Demand
* Sample Events Published by Event Sources

`Ardy` actually support integration with S3, SNS and loudWatch Events. The worst integration of AWS Lambda is the trigger
configuration. You can't see all triggers as a glance in your lambdas configuration and, if you use whe AWS Cli, each trigger
is configured outside AWS Lambda, it's mean, a trigger of S3 is a Event of a S3 bucket; a trigger of SNS is a subscription
of a SNS Topic.

.. tip::
    `Learn more about Versions and Triggers here <http://docs.aws.amazon.com/lambda/latest/dg/intro-invocation-modes.html>`_


Examples
--------

.. code-block:: json

    {
      "version": 1,
      "aws_credentials":{
        "region": "eu-west-1"
      },
      "deploy": {
        "deploy_method": "S3",
        "deploy_bucket": "lambdartefacts",
        "deploy_environments": [
          "dev",
          "pre",
          "pro"
        ],
        "use_alias": false
      },
      "Role": "arn:aws:iam::01234567890:role/service-role/LambdaTest",
      "Runtime": "python3.6",
      "lambdas": [
        {
          "FunctionName": "LambdaExample_S3_1",
          "Handler": "myexamplelambdaproject.lambda1.main.my_handler",
          "Description": "string1",
          "triggers": {
            "s3": [
              {
                "Id": "trigger_from_LambdaExample_S3_7",
                "bucket_name": "lambdatriggers",
                "Events": [
                  "s3:ObjectCreated:*"
                ],
                "Filter": {
                  "Key": {
                    "FilterRules": [
                      {
                        "Name": "Prefix",
                        "Value": "test_"
                      },
                      {
                        "Name": "Suffix",
                        "Value": ""
                      }
                    ]
                  }
                }
              }
            ]
          }
        },
        {
          "FunctionName": "LambdaExample_SNS_2",
          "Handler": "myexamplelambdaproject.lambda2.main.my_handler",
          "triggers": {
            "sns": [
              {
                "TopicArn": "arn:aws:sns:eu-west-1:123456789012:TestLambdas"
              }
            ]
          }
        },
        {
          "FunctionName": "LambdaExample_CWE_3",
          "Handler": "myexamplelambdaproject.lambda3.main.my_handler",
          "triggers": {
            "cloudwatchevent": [
              {
                "Name": "Raise1minute",
                "ScheduleExpression": "cron(* * * * ? *)",
                "State": "DISABLED",
                "Description": "Run every 1 minute"
              }
            ]
          }
        }
      ]
    }