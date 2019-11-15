#!/usr/bin/env bash
set -e

if ! [ -x "$(command -v bumpversion)" ]; then
  echo -e "bumpversion is required, to install it run 'pip install bumpversion'. Aborting." >&2
  exit 1
fi

bumpversion "$1"