# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='alertsd',
    version='0.0.1',
    author='afrank',
    author_email='adam@antilogo.org',
    url='https://github.com/afrank/alertsd',
    description='Maintaining stateful alerts and handling escalations',
    long_description='Alertsd provides a simple way for maintaining state of passive checks and handles escalation.',
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    packages=find_packages('client'),
    package_dir = {'':'client'},
    include_package_data=True,
    install_requires = [
        'simplejson',
        'requests',
    ],

)
