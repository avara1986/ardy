# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os


def touch(fname):
    file = open(fname, "w")
    file.write("Hello World")
    file.close()


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False
