#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "Container is a set of data structures used in openalea such as : graph, grid, topomesh"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs

# find version number in src/openalea/container/version.py
version = {}
with open("src/openalea/container/version.py") as fp:
    exec(fp.read(), version)


setup_kwds = dict(
    name='openalea.container',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Christophe Pradal, revesansparole, ",
    author_email="christophe dot pradal at cirad dot fr, revesansparole@gmail.com, ",
    url='https://github.com/openalea/container',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['include_package_data'] = True
setup_kwds['package_data'] = {'': ['*.pyd', '*.so', '*.zip', '*.png']}

setup_kwds['pylint_packages'] = ['src/container',
                                 'src/container/backend',
                                 'src/container/utils',
                                 'src/container/generator',
                                 'src/openalea/iterator',
                                 'src/openalea/traversal']
setup_kwds['entry_points']['wralea'] = ['container.mesh = container_wralea.mesh']

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
