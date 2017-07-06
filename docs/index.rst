.. Ardy documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ardy (Arthur Hendy)
===================

Ardy is a toolkit to work with AWS Lambas and implement Continuous Integration.
AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources for you. Alas,
AWS Lambda has a very bad GUI interfaces, especially if you work with teams and releases. You can't see at a glance
the triggers you have active, the resources of your AWS Lambda or have a version control.

With `Ardy` you can manage your AWS Lambda with a JSON config file stored in your VCS.



.. warning::
    If you want to work with AWS Lambda, it's recommended read about it. `Ardy` helps and support you to manage your environments but doesn't performs "The black magic" for you.
    You can learn more about AWS Lambda in :doc:`this page </awsdocs>`

Content
-------
.. toctree::
   :maxdepth: 4

   installation
   quickstart
   configuration
   codeexample
   deploy
   commandline
   awsdocs
   howtocontrib
   ardy.core