from setuptools import setup, find_packages

import base

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Emerald',
    version='0.1.0',
    description='A fun 2d RPG game',
    long_description=readme,
    author='Team Frixion',
    author_email='ajcodes22@gmail.com',
    url='https://github.com/',
    license=license,
)