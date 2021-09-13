#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup, Command


# Package meta-data.
NAME = "cipher-common"
DESCRIPTION = "A shared module for use between cipher component"
URL = ""
EMAIL = ""
AUTHOR = "PaulJayP"
REQUIRES_PYTHON = ">=3.9.0"
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}


setup(
    name=NAME,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[],
)
