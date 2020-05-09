#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import find_packages, setup

setup(
    dependency_links=[],
    name="explicitdev",
    version="2020.5.9",
    description="Framework for analyse jira issues and other useful services.",
    author="Sergey Chernyak",
    author_email="chernyaksergey@gmail.com",
    python_requires=">=3.6.0",
    url="https://github.com/onyxim/explicitdev",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["jira", "sqlalchemy", "attrs", "psycopg2", "click", "pytz"],
    extras_require={"dev": ["pipenv-setup", "pytest", "coverage", ], },
    include_package_data=True,
    license="Apache License 2.0",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
