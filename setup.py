#!/usr/bin/env python

from distutils.core import setup

setup(name='itunes-web',
      version='1.0',
      description='control itunes over rest api',
      author='Anuj Patel',
      author_email='patelanuj28@gmail.com',
      url='https://github.com/patelanuj28/itunes-web.git',
      package_dir={'': 'src'},
      py_modules=['itunes_api'],
      license='MIT',
      packages=['itunes-web'],
      install_requires=[
          'bottle',
          'osascript'
      ],
     )