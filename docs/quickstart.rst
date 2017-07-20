Quickstart
==========

Before start working with Ardy or AWS Lambda, if you don’t know anything about AWS Lambda I recommend you the :doc:`AWS documentation </awsdocs>`.

Suppose you have a project with multiple lambas with the following structure:

.. code-block:: bash

   your-project
     ├ lambda1
     │ └ my_handler.py
     ├ lambda2
     │ └ main.py
     ├ lambda3
       └ main.py

To start working with `ardy`, the first step is to create the configuration file with JSON format. The default
file name is **conf.jon**:

.. code-block:: json

    {
      "version": 1,
      "aws_credentials":{
        "aws_access_key_id": "YOUR-AWS-KEY-ID",
        "aws_secret_access_key": "YOUR-AWS-SECRET-KEY",
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
        },
        {
          "FunctionName": "MyOtherOtherLambda",
          "Handler": "your-project.lambda3.main.main.my_handler"
        }
      ]
    }

(See :doc:`more details about the configuration file </configuration>`)

Now, you will have this structure in your project:

.. code-block:: bash

   your-project
     ├ lambda1
     │ └ my_handler.py
     ├ lambda2
     │ └ main.py
     ├ lambda3
     │ └ main.py
     └ config.json

If you want to deploy your AWS Lambdas, you just must run this command in a shell:

.. code-block:: bash

   ardy deploy

Or if you want to deploy a specific list of functions, you can deploy the AWS Lambdas with:

.. code-block:: bash

   ardy deploy MyLambda MyOtherLambda

See :doc:`more details about how to deploy </deploy>`