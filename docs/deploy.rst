Deploy
======

To deploy your project, you can create a script or as a command in a shell (See :doc:`more details about the command line </commandline>`)


.. code-block:: python

    from ardy.core.deploy import Deploy

    if __name__ == '__main__':
        deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)))

        deploy.run("myexamplelambdaproject")
