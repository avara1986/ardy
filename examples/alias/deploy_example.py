# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os

from ardy.core.deploy import Deploy

# App imports

if __name__ == '__main__':
    deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)), lambdas_to_deploy=["LambdaExample1", ],
                    environment="dev")
    deploy.run("myexamplelambdaproject")
