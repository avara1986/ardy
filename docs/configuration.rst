Configuration
=============

All the behavior of `Ardy` toolkit is managed from the configuration file. This file is in **JSON format**.

.. tip::
    Before start, read the `AWS Lambda Best practices <http://docs.aws.amazon.com/lambda/latest/dg/best-practices.html>`_

Base configuration
------------------

* **version:** [REQUIRED] The version of JSON format of `ardy` configuration file. Default 1.
* **aws_credentials:** The best practices are to store your credentials in `your ~/.aws/credentials file <http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration>`_ , but, if it is mandatory, you could set your credentials in the configuration file.

    * **aws_access_key_id:**
    * **aws_secret_access_key:**
    * **region:** [REQUIRED]

Global configuration
--------------------

You can set a global configuration for all your AWS Lambdas. Global configuration is like the keys used to deploy with `API AWS Lambda <http://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html>`_

* **Role:** [REQUIRED] The Amazon Resource Name (ARN) of the IAM role that Lambda assumes when it executes your function to access any other Amazon Web Services (AWS) resources. For more information, see `AWS Lambda: How it Works. <http://docs.aws.amazon.com/lambda/latest/dg/lambda-introduction.html>`_
* **MemorySize:** The amount of memory, in MB, your Lambda function is given
* **Runtime:** The runtime environment for the Lambda function you are uploading
* **Timeout:** The function execution time at which Lambda should terminate the function
* **Publish:** This boolean parameter can be used to request AWS Lambda to create the Lambda function and publish a version as an atomic operation
* **Tags:** The list of tags (key-value pairs) assigned to the new function
* **VpcConfig:** If your Lambda function accesses resources in a VPC, you provide this parameter identifying the list of security group IDs and subnet IDs

Deploy configuration
--------------------

* **deploy:**
    * **deploy_method:** [REQUIRED] String. Must be "`FILE`" or "`S3`". If deploy_method is `S3`, when `ardy` generate the artefact, it will be uploaded to S3. In that case, you must set `deploy_bucket`
    * **deploy_bucket:** String. The S3 bucket if `deploy_method` is S3
    * **version_control:** Not implemented at this moment
    * **deploy_file:** String. If you set a value to this key, `Ardy` doesn't build an artefact, instead, Lambas will be deployed with this file code.
    * **deploy_environments:** List of strings. A map of environments. Each environment represents one possible deployment target. You could set a list of environments to filter. Each environment has a configuration defined for each lambda (see in details below)
    * **use_alias:** [REQUIRED] Bool. This key change the behavior of deploy_environments. If it's False and `deploy_environments` is defined, a lambda will be deployed for each environment. If `use_alias` is True, each lambda will be deployed and an alias will be created for each environment. The alias will be a pointer to a specific `Lambda function version <http://docs.aws.amazon.com/lambda/latest/dg/versioning-aliases.html>`_

AWS Lambda configuration
------------------------

You can set the same keys as in Global Configuration, and it will be overridden. See more `here <http://docs.aws.amazon.com/lambda/latest/dg/API_CreateFunction.html>`_

* **lambdas:** [REQUIRED] List of dictionaries. You can define the key value pair defined below for each AWS Lambda you want to deploy.
    * **FunctionName:** [REQUIRED] String. The name you want to assign to the function you are uploading
    * **Handler:** [REQUIRED] String. The function within your code that Lambda calls to start the execution
    * **Description:** A short, user-defined function description
    * **deploy_environments:** If `use_alias` is False, You can set the same keys as in Global Configuration and Lambda configuration, and it will be overridden. If use_alias is True, one AWS Lambda is deployed and Ardy create an alias pointed to the Lambda Version. Learn :doc:`more details about the alias </configuration.alias>`.
    * **triggers:** :doc:`more details about events and triggers </configuration.triggers>`.

.. tip::
    `Learn more about Versions and Alias here <http://docs.aws.amazon.com/lambda/latest/dg/versioning-aliases.html>`_


Examples
--------

Basic S3
~~~~~~~~

.. code-block:: json

    {
      "version": 1,
      "aws_credentials":{
        "region": "eu-west-1"
      },
      "deploy": {
        "deploy_method": "S3",
        "deploy_bucket": "lambdartefacts",
      },
      "Role": "arn:aws:iam::01234567890:role/service-role/LambdaTest",
      "Runtime": "python3.6",
      "lambdas": [
        {
          "FunctionName": "MyLambda",
          "Handler": "your-project.lambda1.my_handler.my_handler"
        }
      ]
    }

Basic FILE
~~~~~~~~~~

.. code-block:: json

    {
      "version": 1,
      "aws_credentials":{
        "region": "eu-west-1"
      },
      "deploy": {
        "deploy_method": "FILE"
      },
      "Role": "arn:aws:iam::01234567890:role/service-role/LambdaTest",
      "Runtime": "python3.6",
      "lambdas": [
        {
          "FunctionName": "MyLambda",
          "Handler": "your-project.lambda1.my_handler.my_handler"
        }
      ]
    }

Multiple Environments
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "version": 1,
      "aws_credentials":{
        "region": "eu-west-1"
      },
      "deploy": {
        "deploy_method": "FILE",
        "deploy_environments": [
              "dev",
              "pre",
              "pro"
        ]
      },
      "Role": "arn:aws:iam::01234567890:role/service-role/LambdaTest",
      "Runtime": "python3.6",
      "Timeout": 30,
      "lambdas": [
        {
          "FunctionName": "MyLambda",
          "Handler": "your-project.lambda1.my_handler.my_handler",
          "Timeout": 45,
          "deploy_environments": {
            "dev": {
              "FunctionName": "MyLambda_dev",
              "Timeout": 10
            },
            "pre": {
              "FunctionName": "MyLambda_pre"
            },
            "pro": {
              "FunctionName": "MyLambda_pro"
              "Timeout": 300
            }
          }
        }
      ]
    }

Multiple Environments and multiple VPCS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "version": 1,
      "aws_credentials":{
        "region": "eu-west-1"
      },
      "deploy": {
        "deploy_method": "FILE",
        "deploy_environments": [
              "dev",
              "pre",
              "pro"
        ]
      },
      "VpcConfig": {
        "SubnetIds": [
          "subnet-123",
          "subnet-456"
        ],
        "SecurityGroupIds": [
          "sg-789"
        ]
      },
      "Role": "arn:aws:iam::01234567890:role/service-role/LambdaTest",
      "Runtime": "python3.6",
      "lambdas": [
        {
          "FunctionName": "MyLambda",
          "Handler": "your-project.lambda1.my_handler.my_handler",
          "deploy_environments": {
            "dev": {
              "FunctionName": "MyLambda_dev",
            },
            "pre": {
              "FunctionName": "MyLambda_pre"
            },
            "pro": {
              "FunctionName": "MyLambda_pro"
              "Timeout": 300,
              "VpcConfig": {
                "SubnetIds": [
                  "subnet-789"
                ],
                "SecurityGroupIds": [
                  "sg-123"
                ]
              },
            }
          }
        }
      ]
    }

Advanced configuration
----------------------
.. toctree::

      configuration.alias
      configuration.triggers


