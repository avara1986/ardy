# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

import os

from botocore.exceptions import ClientError

from ardy.config import ConfigMixin
from ardy.core.build import Build
from ardy.core.triggers import get_trigger
from ardy.utils.aws import AWSCli
from ardy.utils.log import logger


class Deploy(ConfigMixin):
    build = None

    lambdas_to_deploy = []

    def __init__(self, *args, **kwargs):
        """
        :param args: 
        :param kwargs: 
            * path: string. from ConfigMixin
            * filename: string. from ConfigMixin
            * config
            * lambdas_to_deploy: list.
        """
        self.config = kwargs.get("config", False)
        if not self.config:
            super(Deploy, self).__init__(*args, **kwargs)
        lambdas_to_deploy = kwargs.get("lambdas_to_deploy", [])
        if type(lambdas_to_deploy) is not list:
            lambdas_to_deploy = [lambdas_to_deploy, ]
        self.lambdas_to_deploy = lambdas_to_deploy
        self.awslambda = AWSCli(config=self.config).get_lambda_client()
        self.awss3 = AWSCli(config=self.config).get_s3_resource()
        self.build = Build(config=self.config)

    def run(self, src_project=None, path_to_zip_file=None):
        """Run deploy the lambdas defined in our project.
        Steps:
        * Build Artefact
        * Read file or deploy to S3. It's defined in config["deploy"]["deploy_method"]
        * Reload conf with deploy changes
        * check lambda if exist
            * Create Lambda
            * Update Lambda
                
        
        :param src_project: str. Name of the folder or path of the project where our code lives
        :param path_to_zip_file: str. 
        :return: bool
        """
        if path_to_zip_file:
            code = self.set_artefact_path(path_to_zip_file)
        elif not self.config["deploy"].get("deploy_file", False):
            code = self.build_artefact(src_project)
        else:
            code = self.set_artefact_path(self.config["deploy"].get("deploy_file"))

        self.set_artefact(code=code)
        # Reload conf because each lambda conf need to read again the global conf
        self.config.reload_conf()

        self.deploy()

        return True

    def set_artefact_path(self, path_to_zip_file):
        """
        Set the route to the local file to deploy
        :param path_to_zip_file: 
        :return: 
        """
        self.config["deploy"]["deploy_file"] = path_to_zip_file
        return {'ZipFile': self.build.read(self.config["deploy"]["deploy_file"])}

    def set_artefact(self, code):
        """
        
        :param code: dic. it must be with this shape
        {'ZipFile': } or {'S3Bucket': deploy_bucket, 'S3Key': s3_keyfile, }
        :return: 
        """
        self.config["Code"] = code

    def build_artefact(self, src_project=None):
        """Run deploy the lambdas defined in our project.
        Steps:
        * Build Artefact
        * Read file or deploy to S3. It's defined in config["deploy"]["deploy_method"]

        :param src_project: str. Name of the folder or path of the project where our code lives
        :return: bool
        """
        path_to_zip_file = self.build.run(src_project or self.config.get_projectdir())
        self.set_artefact_path(path_to_zip_file)

        deploy_method = self.config["deploy"]["deploy_method"]

        if deploy_method == "S3":
            deploy_bucket = self.config["deploy"]["deploy_bucket"]
            bucket = self.awss3.Bucket(deploy_bucket)
            try:
                self.awss3.meta.client.head_bucket(Bucket=deploy_bucket)
            except ClientError as e:
                if e.response['Error']['Code'] == "404" or e.response['Error']['Code'] == "NoSuchBucket":
                    region = self.config.get("aws_credentials", {}).get("region", None)

                    logger.info(
                        "Bucket not exist. Creating new one with name {} in region {}".format(deploy_bucket, region))
                    bucket_conf = {}
                    if region:
                        bucket_conf = {"CreateBucketConfiguration": {'LocationConstraint': region}}
                    bucket.wait_until_not_exists()
                    bucket.create(**bucket_conf)
                    bucket.wait_until_exists()

                else:
                    # TODO: handle other errors there
                    pass
            s3_keyfile = self.config["deploy"]["deploy_file"].split(os.path.sep)[-1]
            bucket.put_object(
                Key=s3_keyfile,
                Body=self.build.read(self.config["deploy"]["deploy_file"])

            )
            code = {'S3Bucket': deploy_bucket, 'S3Key': s3_keyfile, }

        elif deploy_method == "FILE":
            code = {'ZipFile': self.build.read(self.config["deploy"]["deploy_file"])}
        else:
            raise Exception("No deploy_method in config")

        return code

    def deploy(self):
        for lambda_funcion in self.config.get_lambdas():
            start_deploy = not len(self.lambdas_to_deploy) or lambda_funcion["FunctionName"] in self.lambdas_to_deploy
            if start_deploy:
                conf = lambda_funcion.get_deploy_conf()
                response = self.remote_get_lambda(**conf)
                if response:
                    remote_conf = response["Configuration"]

                    logger.info("Diferences:")
                    diffkeys = [k for k in remote_conf if
                                conf.get(k, False) != remote_conf.get(k,
                                                                      True) and k not in [
                                    'Code', ]]
                    for k in diffkeys:
                        logger.info((k, ':', conf.get(k, ""), '->', remote_conf.get(k, "")))

                    logger.info("START to update funcion {}".format(conf["FunctionName"]))
                    self.remote_update_conf_lambada(**conf)
                    result = self.remote_update_code_lambada(**conf)

                else:
                    logger.info("START to create funcion {}".format(lambda_funcion["FunctionName"]))
                    result = self.remote_create_lambada(**conf)

                if result['ResponseMetadata']['HTTPStatusCode'] in (201, 200):
                    if self.config["deploy"].get("use_alias", False):
                        result = self.remote_publish_version(**conf)
                        self.remote_update_alias(**{
                            "FunctionName": conf["FunctionName"],
                            "Description": conf["Description"],
                            "FunctionVersion": result["Version"],
                            "Name": self.config["environment"],

                        })
                    logger.info("Updating Triggers for fuction {}".format(lambda_funcion["FunctionName"]))
                    if lambda_funcion.get("triggers", False):

                        for trigger in lambda_funcion["triggers"].keys():
                            trigger_object = get_trigger(trigger, lambda_funcion, result["FunctionArn"])
                            trigger_object.put()

    def remote_get_lambda(self, **kwargs):
        response = False
        try:
            response = self.awslambda.get_function(
                FunctionName=kwargs["FunctionName"],
            )
            tags = response.get("Tags", False)
            if tags:
                response["Configuration"]["Tags"] = tags
        except ClientError as e:
            if e.response['Error']['Code'] == "ResourceNotFoundException":
                return False
            else:
                # TODO: handle other errors there
                pass
        return response

    def remote_list_lambdas(self):
        response = self.awslambda.list_functions(
            MaxItems=100
        )
        return response

    def remote_create_lambada(self, **kwargs):
        response = self.awslambda.create_function(**kwargs)
        return response

    def remote_update_code_lambada(self, **kwargs):
        conf = {"FunctionName": kwargs["FunctionName"]}
        conf.update(kwargs["Code"])
        response = self.awslambda.update_function_code(**conf)

        return response

    def remote_update_conf_lambada(self, **kwargs):
        conf = {k: v for k, v in kwargs.items() if k not in ["Code", "Tags", "Publish"]}
        response = self.awslambda.update_function_configuration(**conf)

        return response

    def remote_publish_version(self, **kwargs):
        conf = {k: v for k, v in kwargs.items() if k in ["FunctionName"]}
        response = self.awslambda.publish_version(**conf)

        return response

    def remote_update_alias(self, **kwargs):
        conf = kwargs
        try:
            logger.info("Update alias {} for function {}"
                        " with version {}".format(conf["Name"],
                                                  conf["FunctionName"],
                                                  conf["FunctionVersion"]))
            response = self.awslambda.update_alias(**conf)
        except ClientError as e:
            if e.response['Error']['Code'] == "ResourceNotFoundException":
                logger.info("Alias {} not exist for function {}. "
                            "Creating new one with version {}".format(conf["Name"],
                                                                      conf["FunctionName"],
                                                                      conf["FunctionVersion"]))

                response = self.awslambda.create_alias(**conf)
            else:
                # TODO: handle other errors there
                pass
        return response
