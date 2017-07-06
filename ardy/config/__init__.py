# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

import json
import os
from abc import ABCMeta

from ardy.config.exceptions import ArdyRequiredKeyError
from ardy.core.exceptions import ArdyLambdaNotExistsError
from ardy.core.exceptions import ArdyNoFileError, ArdyNoDirError, ArdyEnvironmentNotExistsError
from ardy.utils.log import logger


class BaseConfig(dict):
    environment = None

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        super(BaseConfig, self).__init__(**kwargs)

    def __getattr__(self, name, *args, **kwargs):
        return self[name]

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)

    def set_environment(self, environment=False):
        self.environment = environment

    def get_environment(self):
        return self.environment

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class GlobalConfig(BaseConfig):
    """Create the configuration needed to deploy a group of AWS lambda functions
    """
    _DEFAULT_CONFIG_FILE_NAME = "config.json"

    _REQUIRED_LAMBDAS_KEY = "lambdas"

    _REQUIRED_KEYS = ("lambdas",)

    deploy_environments = False

    project_dir = ""

    project_filename = ""

    def __init__(self, *args, **kwargs):
        super(GlobalConfig, self).__init__(*args, **kwargs)
        self.set_projectdir(kwargs.get("path", False))
        self.set_project_config_filename(kwargs.get("filename", False))
        self._set_conf_from_file(environment=kwargs.get("environment", False))
        for key in self._REQUIRED_KEYS:
            if key not in self.keys():
                raise ArdyRequiredKeyError("{} is required to create the configuration".format(key))

    def set_projectdir(self, path=False):
        self.project_dir = os.path.abspath(path or os.getcwd())
        if self.project_dir and os.path.isdir(self.project_dir):
            return True
        raise ArdyNoDirError("Folder {} not exist".format(self.project_dir))

    def get_projectdir(self):
        return self.project_dir

    def set_project_config_filename(self, filename=False):
        self.project_filename = filename or self._DEFAULT_CONFIG_FILE_NAME

    def get_project_config_filename(self):
        return self.project_filename

    def _get_config_file(self):
        return os.path.join(self.get_projectdir(), self.get_project_config_filename())

    def _set_conf_from_file(self, config_file=None, environment=False):
        if not config_file:
            config_file = self._get_config_file()

        if os.path.isfile(config_file):
            logger.debug("Loading configuration from file {}".format(config_file))
            with open(config_file) as data_file:
                config_dict = json.load(data_file)
                self._set_conf_from_dict(config_dict=config_dict, environment=environment)
        else:
            raise ArdyNoFileError("File {} not exist".format(config_file))

    def set_environment(self, environment=False):
        if environment and environment not in self["deploy"]["deploy_environments"]:
            raise ArdyEnvironmentNotExistsError("Environment {} not exists".format(environment))
        self.environment = environment

    def reload_conf(self):
        self._set_conf_from_file()

    def _set_conf_from_dict(self, config_dict, environment=False):
        for key in config_dict:
            self[key] = config_dict[key]
        if environment:
            self.set_environment(environment=environment)
        self[self._REQUIRED_LAMBDAS_KEY] = [
            LambdaConfig(awslambda, self.get_globals(), environment=self.get_environment()) for awslambda in
            config_dict[self._REQUIRED_LAMBDAS_KEY]
        ]

    def get_globals(self):
        return {k: v for k, v in self.items() if k != "lambdas"}

    def get_lambdas(self):
        for awslambda in self["lambdas"]:
            yield awslambda

    def get_lambda_by_name(self, name):
        for i in self.get_lambdas():
            if i["FunctionName"] == name:
                return i
        raise ArdyLambdaNotExistsError("Lambda function {} not exist.".format(name))

    def print_config(self):
        print(json.dumps(self, indent=2))


class LambdaConfig(BaseConfig):
    _DEPLOY_KEYS_BLACKLIST = ["path", "version", "filename", "aws_credentials", "deploy", "triggers",
                              "deploy_environments", "requirements", "environment", "lambdas_to_deploy"]

    def __init__(self, *args, **kwargs):
        super(LambdaConfig, self).__init__(*args, **kwargs)
        self.set_environment(kwargs.get("environment", False))
        self._set_conf_from_dict(args[0], args[1])
        environment_config = args[0].get("deploy_environments", {})
        if self.get_environment() and environment_config:
            self._set_conf_from_dict(environment_config[self.get_environment()], self)

    def _set_conf_from_dict(self, lambda_config, global_config):
        aux_dict = self.merge_dicts(global_config, lambda_config)
        for key in aux_dict:
            self[key] = aux_dict[key]

    def get_deploy_conf(self):
        return {k: v for k, v in self.items() if k not in self._DEPLOY_KEYS_BLACKLIST}

    def merge_dicts(self, x, y):
        """
        if sys.version_info >= (3,5):
            return {**x, **y}
        else:
        """
        z = x.copy()
        z.update(y)
        return z


class ConfigMixin(object):
    def __init__(self, *args, **kwargs):
        super(ConfigMixin, self).__init__()
        logger.debug("[{}] loading config...".format(self.__class__, ))
        self.config = GlobalConfig(*args, **kwargs)
