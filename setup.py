#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
    install_requires = [i for i in install_requires if '://' not in i]

VERSION = '0.0.0.DEV0'

setup(
    name='pyampd',
    version=VERSION,
    packages=find_packages(exclude=('tests', )),
    entry_points={'console_scripts': []},
    include_package_data=True,
    zip_safe=False,
    description='Peak detection using AMPD and ASS-AMPD algorithms',
    author='Igor Gotlibovych',
    author_email='igor.gotlibovych@gmail.com',
    license='MIT',
    install_requires=install_requires,
    extras_require={},
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
