#!/usr/bin/env bash

set -e

if [[ "$1" != "" ]]
then
    pytest -k $1 tests
else
    pytest tests
fi
