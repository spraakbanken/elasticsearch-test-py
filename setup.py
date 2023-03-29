# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Database",
    "Topic :: Software Development",
    "Topic :: Software Development :: Testing",
]

setup(
    name='elasticsearch-test-py',
    version='1.2.0',
    description='Start Elasticsearch with Python (for testing or other purposes)',
    long_description=open('README.rst').read(),
    classifiers=classifiers,
    keywords=[],
    author='Språkbanken',
    author_email='maria.ohrman@gu.se',
    url='https://github.com/spraakbanken/elasticsearch-test-py',
    license='MIT License',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
    ],
    extras_require=dict(
        testing=[
            'tox',
            'pytest',
            'requests',
            'flake8'
        ],
    ),

)
