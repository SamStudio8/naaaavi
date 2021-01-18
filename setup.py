#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from naaaavi import version

requirements = [
]

test_requirements = [

]

setuptools.setup(
    name="naaaavi",
    version=version.__version__,
    url="https://github.com/samstudio8/naaaavi",

    description="",
    long_description="",

    author="Sam Nicholls",
    author_email="sam@samnicholls.net",

    maintainer="Sam Nicholls",
    maintainer_email="sam@samnicholls.net",

    packages=setuptools.find_packages(),
    install_requires=requirements,

    entry_points = {
        'console_scripts': [
            'naaaavi = naaaavi.client:cli',
            'navi = naaaavi.client:cli',
        ]
    },

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
    ],

    test_suite="tests",
    tests_require=test_requirements,

)
