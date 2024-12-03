"""Setup file for the package"""
from setuptools import setup

setup(
    name='sib',
    version='0.2.1',
    packages=['sib/literature'],
    install_requires=['requests', 'openai'],
)
