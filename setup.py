from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as fp:
    install_requires = fp.read()

setup(
    name='pycpt',
    version='0.2.0',
    author='Jonas Sølvsteen',
    author_email='j08lue@gmail.com',
    packages=find_packages(),
    description='Read, modify, and display color maps from .cpt files',
    install_requires=install_requires,
    extras_require={
        'test': [
            'pytest>=3.5',
            'pytest-cov',
            'codecov'
        ]
    }
)
