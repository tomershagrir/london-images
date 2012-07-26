import os

# Downloads setuptools if not find it before try to import
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

packages = ['images']

setup(
    name='London Images',
    version=0.1,
    #url='',
    author="Juan Pablo Romero",
    license="BSD License",
    packages=packages,
    install_requires=['Pillow'],
)

