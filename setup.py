#!/usr/bin/env python
from os import path

from setuptools import setup

from belvo import __version__

here = path.abspath(path.dirname(__file__))


with open(path.join(here, "requirements/base.txt")) as f:
    requirements = f.read().splitlines()


with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    version=__version__,
    python_requires=">=3.5, <4",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["belvo-cli=belvo.console:main"]},
)
