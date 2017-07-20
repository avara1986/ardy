.. Ardy documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ardy (Arthur Hendy)
===================

Ardy is a toolkit to work with AWS Lambda  implementing Continuous Integration.
AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the
underlying compute resources for you. Alas, AWS Lambda has a very bad GUI interface, especially if you work with teams
and releases. You can’t easily see at a glance the active triggers you have, the resources of your AWS Lambda or have a
version control.

With `Ardy` you can manage your AWS Lambda with a JSON config file stored in your VCS.



.. warning::
    If you want to work with AWS Lambda, it’s recommended to read about it. `Ardy` helps and supports you to manage
    environments but doesn’t performs "The black magic" for you. You can learn more about AWS Lambda in
    :doc:`this page </awsdocs>`

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