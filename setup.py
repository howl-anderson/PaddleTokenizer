#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

# without tensorflow by default
install_requires = ["paddlepaddle<2.0", "tokenizer_tools", "flask", "Flask-Cors"]


setup_requirements = ["pytest-runner"]

test_requirements = ["pytest", "pytest-helpers-namespace"]

setup(
    author="Xiaoquan Kong",
    author_email="u1mail2me@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="A tokenizer write in PaddlePaddle",
    install_requires=install_requires,
    license="AGPL license",
    long_description="A tokenizer write in PaddlePaddle",
    include_package_data=True,
    keywords="paddle_tokenizer",
    name="paddle_tokenizer",
    packages=find_packages(include=["paddle_tokenizer", "paddle_tokenizer.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/howlandersonn/PaddleTokenizer",
    version="0.1.0",
    zip_safe=False,
)
