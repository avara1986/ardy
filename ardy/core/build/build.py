# coding=utf-8
# python imports
from __future__ import unicode_literals, print_function

import datetime
import os
import zipfile
from shutil import copy2
from tempfile import mkdtemp

import pip

from ardy.config import ConfigMixin
from ardy.core.exceptions import ArdyNoFileError
from ardy.utils.log import logger


class Build(ConfigMixin):
    src_path = ""

    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", False)
        if not self.config:
            super(Build, self).__init__(*args, **kwargs)

    def mkdir(self, path):
        path = os.path.join(self.config.get_projectdir(), path)
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return False

    @staticmethod
    def read(path, loader=None):
        with open(path, "rb") as fh:
            if not loader:
                return fh.read()
            return loader(fh.read())

    @staticmethod
    def timestamp(fmt='%Y-%m-%d-%H%M%S'):
        now = datetime.datetime.utcnow()
        return now.strftime(fmt)

    def create_artefact(self, src, dest, filename):
        if not os.path.isabs(dest):
            dest = os.path.join(self.config.get_projectdir(), dest)
        dest = os.path.abspath(dest)
        if not os.path.isabs(src):
            src = os.path.join(self.config.get_projectdir(), src)
        relroot = os.path.abspath(src)

        output = os.path.join(dest, filename)
        excluded_folders = ["dist", ]
        excluded_files = []
        if not os.path.isdir(src) and not os.path.isfile(src):
            raise ArdyNoFileError("{} not exists".format(src))
        with zipfile.ZipFile(output, 'a', compression=zipfile.ZIP_DEFLATED) as zf:
            for root, subdirs, files in os.walk(src):
                excluded_dirs = []
                for subdir in subdirs:
                    for excluded in excluded_folders:
                        if subdir.startswith(excluded):
                            excluded_dirs.append(subdir)
                for excluded in excluded_dirs:
                    subdirs.remove(excluded)
                try:
                    dir_path = os.path.relpath(root, relroot)
                    dir_path = os.path.normpath(
                        os.path.splitdrive(dir_path)[1]
                    )
                    while dir_path[0] in (os.sep, os.altsep):
                        dir_path = dir_path[1:]
                    dir_path += '/'
                    zf.getinfo(dir_path)
                except KeyError:
                    zf.write(root, dir_path)

                for filename in files:
                    if filename not in excluded_files:
                        filepath = os.path.join(root, filename)
                        if os.path.isfile(filepath):
                            arcname = os.path.join(
                                os.path.relpath(root, relroot), filename)
                            try:
                                zf.getinfo(arcname)
                            except KeyError:
                                zf.write(filepath, arcname)
        return output

    def copytree(self, src, dst, symlinks=False, ignore=None):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                self.copytree(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                    copy2(s, d)

    def set_src_path(self, src_folder):
        self.src_path = os.path.abspath(os.path.join(self.config.get_projectdir(), src_folder))

    def get_src_path(self):
        return self.src_path

    def run(self, src_folder, requirements="requirements.txt", local_package=None):
        """Builds the file bundle.
        :param str src:
           The path to your Lambda ready project (folder must contain a valid
            config.yaml and handler module (e.g.: service.py).
        :param str local_package:
            The path to a local package with should be included in the deploy as
            well (and/or is not available on PyPi)
        """
        self.set_src_path(src_folder)

        if not os.path.isdir(self.get_src_path()):
            raise ArdyNoFileError("File {} not exist".format(self.get_src_path()))
        # Get the absolute path to the output directory and create it if it doesn't
        # already exist.
        dist_directory = 'dist'
        path_to_dist = os.path.join(self.get_src_path(), dist_directory)
        self.mkdir(path_to_dist)

        # Combine the name of the Lambda function with the current timestamp to use
        # for the output filename.
        output_filename = "{0}.zip".format(self.timestamp())

        path_to_temp = mkdtemp(prefix='aws-lambda')
        self.pip_install_to_target(path_to_temp,
                                   requirements=requirements,
                                   local_package=local_package)

        if os.path.isabs(src_folder):
            src_folder = src_folder.split(os.sep)[-1]

        self.copytree(self.get_src_path(), os.path.join(path_to_temp, src_folder))

        # Zip them together into a single file.
        # TODO: Delete temp directory created once the archive has been compiled.
        path_to_zip_file = self.create_artefact(path_to_temp, path_to_dist, output_filename)
        return path_to_zip_file

    def _install_packages(self, path, packages):
        """Install all packages listed to the target directory.
        Ignores any package that includes Python itself and python-lambda as well
        since its only needed for deploying and not running the code
        :param str path:
            Path to copy installed pip packages to.
        :param list packages:
            A list of packages to be installed via pip.
        """

        def _filter_blacklist(package):
            blacklist = ["-i", "#", "Python==", "ardy=="]
            return all(package.startswith(entry.encode()) is False for entry in blacklist)

        filtered_packages = filter(_filter_blacklist, packages)
        # print([package for package in filtered_packages])
        for package in filtered_packages:
            if package.startswith(b'-e '):
                package = package.replace('-e ', '')

            logger.info('Installing {package}'.format(package=package))
            pip.main(['install', package, '-t', path, '--ignore-installed', '-q'])

    def pip_install_to_target(self, path, requirements="", local_package=None):
        """For a given active virtualenv, gather all installed pip packages then
        copy (re-install) them to the path provided.
        :param str path:
            Path to copy installed pip packages to.
        :param bool requirements:
            If set, only the packages in the requirements.txt file are installed.
            The requirements.txt file needs to be in the same directory as the
            project which shall be deployed.
            Defaults to false and installs all pacakges found via pip freeze if
            not set.
        :param str local_package:
            The path to a local package with should be included in the deploy as
            well (and/or is not available on PyPi)
        """
        packages = []
        if not requirements:
            logger.debug('Gathering pip packages')
            # packages.extend(pip.operations.freeze.freeze())
            pass
        else:
            requirements_path = os.path.join(self.get_src_path(), requirements)
            logger.debug('Gathering packages from requirements: {}'.format(requirements_path))
            if os.path.isfile(requirements_path):
                data = self.read(requirements_path)
                packages.extend(data.splitlines())
            else:
                logger.debug('No requirements file in {}'.format(requirements_path))

        if local_package is not None:
            if not isinstance(local_package, (list, tuple)):
                local_package = [local_package]
            for l_package in local_package:
                packages.append(l_package)
        self._install_packages(path, packages)
