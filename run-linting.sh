#!/usr/bin/env bash

set -e

if [[ "$1" = "yes" ]]
then
    isort -rc .
    black .
else
    isort --check-only -df -rc .
    black --check .
fi
