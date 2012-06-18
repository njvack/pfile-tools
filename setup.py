from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pfile-tools',
    version='0.1dev',
    packages=['pfile_tools',],
    license='BSD License',
    long_description=read('README.textile'),
)