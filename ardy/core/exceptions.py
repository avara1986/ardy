# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function


class ArdyNoFileError(Exception):
    pass


class ArdyNoDirError(Exception):
    pass


class ArdyLambdaNotExistsError(Exception):
    pass


class ArdyEnvironmentNotExistsError(Exception):
    pass


class ArdyAwsError(Exception):
    pass


class ArdyNoArtefactError(Exception):
    pass


class ArdyNotImplementError(Exception):
    pass
