#!/usr/bin/env bash

set -e
rm -rf tmp/
venv/bin/python3 manage.py cov

