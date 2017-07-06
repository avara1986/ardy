#!/bin/sh
coverage erase
tox
coverage combine
coverage report -m
coverage html
