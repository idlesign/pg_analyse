import io
import os
import re
import sys

from setuptools import setup, find_packages

try:
    import psycopg2
    install_requires = []

except ImportError:
    install_requires = ['psycopg2-binary']  # To not to build on install.


PATH_BASE = os.path.dirname(__file__)


def check_submodule():
    if not os.path.exists(os.path.join(PATH_BASE, 'pg_analyse', 'sql', 'contrib', 'index_health', 'sql')):
        raise Exception('Submodules not initialized. Use "$ git submodule update --init" after that retry.')


check_submodule()


def read_file(fpath):
    """Reads a file within package directories."""
    with io.open(os.path.join(PATH_BASE, fpath)) as f:
        return f.read()


def get_version():
    """Returns version number, without module import (which can lead to ImportError
    if some dependencies are unavailable before install."""
    contents = read_file(os.path.join('pg_analyse', '__init__.py'))
    version = re.search('VERSION = \(([^)]+)\)', contents)
    version = version.group(1).replace(', ', '.').strip()
    return version


setup(
    name='pg_analyse',
    version=get_version(),
    url='https://github.com/idlesign/pg_analyse',

    description='Tools to gather useful information from PostgreSQL',
    long_description=read_file('README.rst'),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,

    install_requires=install_requires,

    extras_require={
        'cli': [
            'click',
            'tabulate',
        ],
    },

    setup_requires=(['pytest-runner'] if 'test' in sys.argv else []) + [],

    entry_points={
        'console_scripts': ['pg_analyse = pg_analyse.cli:main'],
    },

    python_requires='>=3.6',

    test_suite='tests',

    tests_require=[
        'pytest',
        'tabulate',
    ],

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License'
    ],
)
