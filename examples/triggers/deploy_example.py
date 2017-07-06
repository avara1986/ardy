# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os

# App imports
from ardy.core.deploy import Deploy

if __name__ == '__main__':
    deploy = Deploy(path=os.path.dirname(os.path.abspath(__file__)))

    deploy.run("myexamplelambdaproject")
