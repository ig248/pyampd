#!/usr/bin/env python
# -*- coding: utf-8 -*

import os

from setuptools import find_packages, setup

install_requires = ['numpy', 'scipy']

VERSION = '0.0.1'

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pyampd',
    version=VERSION,
    description='Peak detection using AMPD and ASS-AMPD algorithms',
    url='https://github.com/ig248/kerashistoryplot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests', )),
    entry_points={'console_scripts': []},
    include_package_data=True,
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
