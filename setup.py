# -*- coding: utf-8 -*-
# Copyright (c) 2017 by Alberto Vara <a.vara.1986@gmail.com>
import codecs
import os

from setuptools import setup, find_packages

version = __import__('ardy').__version__
author = __import__('ardy').__author__
author_email = __import__('ardy').__email__

if os.path.exists('README.rst'):
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See https://github.com/avara1986/ardy'

setup(
    name="Ardy",
    version=version,
    author=author,
    author_email=author_email,
    description="AWS Lambda toolkit",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
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
