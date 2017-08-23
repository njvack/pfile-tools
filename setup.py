#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='pfile-tools',
    version='0.5.0',
    author='Nathan Vack',
    author_email='njvack@wisc.edu',
    license='BSD License',
    url='https://github.com/njvack/pfile-tools',
    packages=['pfile_tools'],
    entry_points={
        'console_scripts': [
            'dump_pfile_header = pfile_tools.scripts.dump_pfile_header:main',
            'anonymize_pfile = pfile_tools.scripts.anonymize_pfile:main'
        ]}
    )




# setup(
#     name='pfile-tools',
#     version=pfile_tools.VERSION,
#     packages=setuptools.find_packages(),
#     data_files=[('', ['distribute_setup.py'])],
#     license='BSD License',
#     long_description=read('README'),
#     url="https://github.com/njvack/pfile-tools",
#     author="Nathan Vack",
#     author_email="njvack@wisc.edu",
#     entry_points = {
#         'console_scripts': [
#             'dump_pfile_header = pfile_tools.scripts.dump_pfile_header:main',
#             'anonymize_pfile = pfile_tools.scripts.anonymize_pfile:main'
#         ]
#     }
# )