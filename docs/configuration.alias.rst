Alias and Versions
==================

Environments
------------

To use Alias with Ardy, you must set True "use_alias". ¿What is the difference?

If not use alias, when you deploy, for example, this configuration:

.. code-block:: json

    {
      "FunctionName": "LambdaExample1",
      "Handler": "myexamplelambdaproject.lambda1.main.my_handler",
      "deploy_environments": {
        "dev": {"FunctionName": "LambdaExample1_dev"},
        "pre": {"FunctionName": "LambdaExample1_pre",},
        "pro": {"FunctionName": "LambdaExample1_pro",}
      }
    }

When you run this 3 commands:

.. code-block:: bash

    ardy deploy LambdaExample1 dev
    ardy deploy LambdaExample1 pre
    ardy deploy LambdaExample1 pro

`Ardy` create a AWS Lambda for each environment ("LambdaExample1_dev", "LambdaExample1_pre", "LambdaExample1_pro"). Each AWS Lambda could has a specific configuration (I.E: Set different VPCS for each environment, different runtime...)

.. image:: ../_static/aws_environments.png


Alias
-----
If use alias,  with this configuration:

.. code-block:: json

    {
      "FunctionName": "LambdaExample1",
      "Handler": "myexamplelambdaproject.lambda1.main.my_handler",
      "deploy_environments": {
        "dev": {"Description": "AWS lambda LambdaExample1 DEV environment"},
        "pre": {},
        "pro": {"Description": "AWS lambda LambdaExample1 PRO environment"}
      }
    }

When you run this 3 commands:

.. code-block:: bash

    ardy deploy LambdaExample1 dev
    ardy deploy LambdaExample1 pro

`Ardy` create just one AWS Lambda "LambdaExample1", increment its version and creates 2 alias pointed to diferents versions of the lambda.

.. image:: ../_static/aws_alias0.png

.. image:: ../_static/aws_alias1.png

.. image:: ../_static/aws_alias2.png


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
        "use_alias": true
      },
      "Role": "arn:aws:iam::01234567890:role/service-role/LambdaTest",
      "Runtime": "python3.6",
      "lambdas": [
        {
          "FunctionName": "LambdaExample1",
          "Handler": "myexamplelambdaproject.lambda1.main.my_handler",
          "deploy_environments": {
            "dev": {},
            "pre": {},
            "pro": {}
          }
        },
        {
          "FunctionName": "LambdaExample2",
          "Handler": "myexamplelambdaproject.lambda2.main.my_handler",
          "deploy_environments": {
            "dev": {},
            "pre": {},
            "pro": {}
          }
        },
        {
          "FunctionName": "LambdaExample3",
          "Handler": "myexamplelambdaproject.lambda3.main.my_handler",
          "deploy_environments": {
            "dev": {},
            "pre": {},
            "pro": {}
          }
        }
      ]
    }