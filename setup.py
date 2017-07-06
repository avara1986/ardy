# -*- coding: utf-8 -*-
# Copyright (c) 2017 by Alberto Vara <a.vara.1986@gmail.com>
import os
from setuptools import setup, find_packages


def read(file):
    return open(os.path.join(os.path.dirname(__file__), file))


setup(
    name="Ardy",
    version="0.0.1",
    author="Alberto Vara",
    author_email="a.vara.1986@gmail.com",
    description="AWS Lambda toolkit",
    long_description=(read('README.rst').read() + '\n\n' + read('CHANGES.rst').read()),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5"
        "Programming Language :: Python :: 3.6"
    ],
    license="MIT",
    platforms=["any"],
    keywords="python, aws, lambda",
    url='https://github.com/avara1986/ardy.git',
    test_suite='nose.collector',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ardy = ardy.core.cmd.main:Command'
        ]
    },
    install_requires=[
        "boto3>=1.4.4"
    ],
    zip_safe=True,
)
