from distribute_setup import use_setuptools
use_setuptools()
from distutils.core import setup

setup(
    name='pfile-tools',
    version='0.1dev',
    packages=['pfile_tools',],
    license='BSD License',
    long_description=open('README.textile').read(),
)