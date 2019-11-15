#!/usr/bin/env bash

set -ex

if [[ "$1" = "yes" ]]
then
    isort -rc .
    black .
else
    isort --check-only -df -rc .
    black --check .
    mypy .
    flake8 .
fi
