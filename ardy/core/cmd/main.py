#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import argparse
import sys

from ardy.config import GlobalConfig
from ardy.core.build import Build
from ardy.core.deploy import Deploy


class Command(object):
    config = None

    parser = None

    args = []

    def __init__(self, *args, **kwargs):
        arguments = kwargs.get("arguments", False)
        if not arguments:
            arguments = sys.argv[1:]

        self.parser = self.init_config(arguments)

        commands = self.parser.add_subparsers(title="Commands", description='Available commands', dest='command_name')

        # Add deploy commands
        parser_deploy = commands.add_parser('deploy', help='Upload functions to AWS Lambda')
        parser_deploy.add_argument("lambdafunctions", default="_ALL_", nargs='*', type=str, help='Lambda(s) to deploy')
        parser_deploy.add_argument("-z", "--zipfile", help="Path and filename of artefact to deploy")

        environments = self.config["deploy"].get("deploy_environments", [])
        if environments:
            parser_deploy.add_argument("environment", choices=environments, type=str,
                                       help='Environment where deploy: {}'.format(environments))

        # Add invoke commands
        parser_invoke = commands.add_parser('invoke', help='Invoke a functions from AWS Lambda')
        parser_invoke.add_argument("-l", "--lambda-function", help="lambda")

        # Add build commands
        parser_build = commands.add_parser('build',
                                           help='Create an artefact and Upload to S3 if S3 is configured (See config)')
        parser_build.add_argument("-r", "--requirements", help="Path and filename of the python project")
        self.args = self.parser.parse_args(arguments)
        self.parse_commandline()

    @property
    def parser_base(self):
        parser = argparse.ArgumentParser(description='Ardy. AWS Lambda Toolkit')
        parser.add_argument("-f", "--conffile", help="Name to the project config file")
        parser.add_argument("-p", "--project", help="Project path")
        return parser

    def init_config(self, arguments):
        # TODO: refactor this method... sooo ugly :S
        parser = self.parser_base
        parser.add_argument('args', nargs=argparse.REMAINDER)
        base_parser = parser.parse_args(arguments)

        params = {}
        if getattr(base_parser, "project", False) and base_parser.project is not None:
            params["path"] = base_parser.project

        if getattr(base_parser, "conffile", False) and base_parser.conffile is not None:
            params["filename"] = base_parser.conffile

        self.config = GlobalConfig(**params)

        return self.parser_base

    def parse_commandline(self):
        params = {}
        run_params = {}

        if self.args.command_name == "deploy":
            if self.args.lambdafunctions and self.args.lambdafunctions is not "_ALL_":
                params["lambdas_to_deploy"] = self.args.lambdafunctions
            if getattr(self.args, "environment", False):
                params["environment"] = self.args.environment
            if getattr(self.args, "zipfile", False):
                run_params["path_to_zip_file"] = self.args.zipfile

            deploy = Deploy(config=self.config, **params)
            deploy.run(**run_params)

        elif self.args.command_name == "invoke":
            pass
        elif self.args.command_name == "build":
            if getattr(self.args, "requirements", False):
                run_params["requirements"] = self.args.requirements
            build = Build(config=self.config)
            build.run(**params)
        else:
            self.parser.print_help()


if __name__ == '__main__':
    cmd = Command(arguments=sys.argv[1:])
