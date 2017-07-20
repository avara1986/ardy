Command Line
============

`Ardy`'s command line, by default, search a *config.json* at the same path that the command is running. But you can set a
different path with the argument *-p*.

optional arguments:
  -h, --help            show this help message and exit
  -f CONFFILE, --conffile CONFFILE
                        Name to the project config file
  -p PROJECT, --project PROJECT
                        Project path

Commands:
  - *deploy:* Upload functions to AWS Lambda
  - *invoke:* Invoke functions from AWS Lambda
  - *build:* Create an artefact

If you want to deploy *all your AWS Lambdas* defined in your *config.json* file

.. code-block:: bash

   ardy deploy

Or if you want to deploy a specific list of functions, you can deploy the AWS Lambdas with:

.. code-block:: bash

   ardy deploy MyLambda MyOtherLambda

You can deploy only an environment:

.. code-block:: bash

   ardy deploy MyLambda MyOtherLambda dev
   ardy deploy MyLambda MyOtherLambda pre
   ardy deploy MyLambda pro

Example Scenario
----------------

You have a project with this structure:

.. code-block:: bash

   main-project
   ├ lambda-subproject
   │ ├ lambda1
   │ │ └ my_handler.py
   │ ├ lambda2
   │ │ └ main.py
   │ ├ lambda3
   │ │ └ main.py
   └ config.json

The path of your project is `/var/www/main-project/lambda-subproject` and a config.json like that:

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
        },
        {
          "FunctionName": "MyOtherLambda",
          "Handler": "your-project.lambda2.main.main.my_handler"
        }
      ]
    }

You're in `/var/www/main-project/`, and want to deploy `MyLambda`:

.. code-block:: bash

   ardy -p lambda-subproject deploy MyLambda

But, if you're in `/home/Caerbannog_user/`, and want to deploy `MyLambda`:

.. code-block:: bash

   ardy -f /var/www/main-project/config.json -p /var/www/main-project/lambda-subproject deploy MyLambda