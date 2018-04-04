#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


setup(
    name='dnsplug',
    version='0.1.0',
    license='GPL',
    description='a thin wrapper and caching layer for dns lookups',
    author='Noa Resare',
    author_email='noa@resare.com',
    url='https://github.com/nresare/dnsplug',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,
)
