#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = ["gdanmaku"]
requires = ["requests"]

with open("README.md") as f:
    readme = f.read()

setup(
    name="gdanmaku",
    version="0.2-dev",
    description="Display danmaku on any screen",
    long_description=readme,
    author="Justin Wong",
    author_email="justin.w.xd@gmail.com",
    url="https://github.com/tuna/gdanmaku/",
    packages=packages,
    package_data={'': ['LICENCE', ], 'gdanmaku': [os.path.join('images', '*.png'), ]},
    package_dir={'gdanmaku': 'gdanmaku'},
    include_package_data=True,
    install_requires=requires,
    license="GPLv3",
    entry_points={
        'console_scripts': ['gdanmaku = gdanmaku.danmaku:main'],
    },
)

# vim: ts=4 sw=4 sts=4 expandtab
