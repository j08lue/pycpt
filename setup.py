try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name = 'pycpt',
      version = '0.2.0',
      author = 'Jonas Bluethgen',
      author_email = 'bluthgen@nbi.ku.dk',
      packages = ['pycpt'],
      url = 'http://www.gfy.ku.dk/~bluthgen',
      license = 'LICENSE.txt',
      description = 'Read, modify, and display color maps from .cpt files',
      long_description = open('README.md').read(),
      )
