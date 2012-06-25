#!/usr/bin/env python
from distribute_setup import use_setuptools
use_setuptools()
import setuptools
from setuptools import setup
import os

import pfile_tools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pfile-tools',
    version=pfile_tools.VERSION,
    packages=setuptools.find_packages(),
    data_files=[('', ['distribute_setup.py'])],
    license='BSD License',
    long_description=read('README'),
    url="https://github.com/njvack/pfile-tools",
    author="Nathan Vack",
    author_email="njvack@wisc.edu",
    entry_points = {
        'console_scripts': [
            'dump_pfile_header = pfile_tools.scripts.dump_pfile_header:main',
            'anonymize_pfile = pfile_tools.scripts.anonymize_pfile:main'
        ]
    }
)