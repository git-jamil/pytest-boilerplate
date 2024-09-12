#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import setuptools


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setuptools.setup(
    name="pytest-boilerplate",
    version="0.0.2",
    author="DEVxHUB",
    author_email="tech@devxhub.com",
    maintainer="DEVxHUB",
    maintainer_email="tech@devxhub.com",
    license="MIT",
    url="https://github.com/devxhub/pytest-boilerplate",
    project_urls={
        "Repository": "https://github.com/devxhub/pytest-boilerplate",
        "Issues": "https://github.com/devxhub/pytest-boilerplate/issues",
    },
    description="The pytest plugin for your devxhub_python templates. 🍪",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "devxhub_python>=0.5.0",  # uses pyyaml
        "pytest>=3.9.0",  # adds tmp_path fixtures
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
        "Framework :: Pytest",
    ],
    entry_points={"pytest11": ["boilerplate = pytest_boilerplate.plugin"]},
    keywords=["devxhub_python", "pytest"],
)
