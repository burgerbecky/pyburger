#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger file functions

Copyright 2013-2018 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import burger

########################################


def test_get_sdks_folder(tmpdir):
	"""
	Test burger.get_sdks_folder()
	"""

	saved = os.getenv('BURGER_SDKS', default=None)
	saved_dir = os.getcwd()

	# Test with current value
	if saved:
		assert burger.get_sdks_folder() == saved

	# Test folder override
	assert burger.get_sdks_folder(refresh=True, folder='test') == 'test'
	assert burger.get_sdks_folder() == 'test'

	# Test reading BURGER_SDKS
	os.environ['BURGER_SDKS'] = 'newvalue'
	assert burger.get_sdks_folder(refresh=True) == 'newvalue'
	assert burger.get_sdks_folder() == 'newvalue'

	# Test with fake 'sdks' folder

	os.environ.pop('BURGER_SDKS', None)
	tmpdir.mkdir('a')
	tmpdir.mkdir('a', 'b')
	tmpdir.mkdir('a', 'b', 'sdks')
	tmpdir.mkdir('a', 'b', 'sdks', 'c')
	tmpdir.mkdir('a', 'b', 'sdks', 'c', 'd')
	os.chdir(os.path.join(str(tmpdir), 'a', 'b', 'sdks', 'c', 'd'))
	assert burger.get_sdks_folder(refresh=True) == \
		os.path.join(str(tmpdir), 'a', 'b', 'sdks')

	# Cleanup
	os.chdir(saved_dir)
	tmpdir.remove()

	# Restore the cache to the correct value
	if saved:
		os.putenv('BURGER_SDKS', saved)
		burger.get_sdks_folder(refresh=True, folder=saved)
