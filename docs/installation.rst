Installation
============

Install the latest Ardy release via pip:

.. code-block:: bash

   pip install ardy

You may also install a specific version:

.. code-block:: bash

   pip install ardy==0.0.1


Credentials
-----------

Before you can deploy an application, be sure you have credentials configured. If you have previously configured your machine to run boto3 (the AWS SDK for Python) or the AWS CLI then you can skip this section.

If this is your first time configuring credentials for AWS you can follow these steps to quickly get started:


.. code-block:: bash
   $ mkdir ~/.aws
   $ cat >> ~/.aws/credentials
   [default]
   aws_access_key_id=YOUR_ACCESS_KEY_HERE
   aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
   region=YOUR_REGION (such as us-west-2, us-west-1, etc)