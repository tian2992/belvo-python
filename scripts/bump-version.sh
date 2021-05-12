#!/usr/bin/env bash
set -e

if ! [ -x "$(command -v bump2version)" ]; then
  echo -e "bump2version is required, to install it run 'pip install bump2version'. Aborting." >&2
  exit 1
fi

bump2version "$1"
