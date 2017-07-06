# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function, absolute_import

import os
import zipfile

from tests.utils import touch


class MockContext:
    invoked_function_arn = ""

    def __init__(self, function_name):
        self.invoked_function_arn = "arn: aws:lambda:eu-west-1:123456789:function:{}".format(function_name)


class MockZipFile:
    @classmethod
    def create_zip(cls, fname):
        example_file = fname + ".txt"
        zip_file = fname + ".zip"
        touch(example_file)
        zfh = zipfile.ZipFile(fname + ".zip", 'w', zipfile.ZIP_DEFLATED)
        zfh.write(example_file)
        zfh.close()
        os.remove(example_file)
        return zip_file

    @classmethod
    def read_file(cls, path):
        with open(path, "rb") as fh:
            return fh.read()
        return False

    @classmethod
    def touch(cls, fname):
        file = open(fname, "w")
        file.write("Hello World")
        file.close()
