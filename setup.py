#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build the egg file for burger for python

Copyright 2013-2018 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

from __future__ import absolute_import, print_function, unicode_literals
from setuptools import setup
import burger

#
# Create the dependency list
#

install_requires = [		#pylint: disable=C0103
	'setuptools >= 0.7.0'
]

#
# Parms for setup
#

setup_args = dict(			#pylint: disable=C0103

	name='burger',
	version=burger.__version__,

	#
	# Use the readme as the long description
	#

	description=burger.__summary__,
	long_description=open('README.rst').read(),
	license=burger.__license__,
	url=burger.__uri__,

	author=burger.__author__,
	author_email=burger.__email__,

	keywords='burger perforce burgerlib development',
	platforms='any',
	install_requires=install_requires,

	classifiers=
	[ \
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Topic :: Software Development',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Natural Language :: English',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6'
	],
	py_modules=['burger'],
)

#
# Perform the setup
#

if __name__ == '__main__':
	setup(**setup_args)
