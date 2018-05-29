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


def test_traverse_directory(tmpdir):
	"""
	Test burger.traverse_directory()
	"""

	# Files to scan for
	fooey1 = 'foo1.txt'
	fooey2 = 'foo2.txt'

	# Create the folder a/b/c/d
	dir1 = tmpdir
	dir2 = dir1.mkdir('a')
	dir3 = dir2.mkdir('b')
	dir4 = dir3.mkdir('c')
	dir5 = dir4.mkdir('d')

	# Perform tests that result in empty lists
	temp_list = burger.traverse_directory(str(dir5), fooey1, False)
	assert not temp_list
	temp_list = burger.traverse_directory(str(dir5), (fooey1, fooey2), False)
	assert not temp_list
	temp_list = burger.traverse_directory(str(dir5), [fooey1, fooey2], False)
	assert not temp_list
	temp_list = burger.traverse_directory(str(dir5), {fooey1, fooey2}, False)
	assert not temp_list

	# Add some files
	dir2.join(fooey1).write(fooey1)
	dir4.join(fooey2).write(fooey2)
	fooey1path = os.path.join(str(dir2), fooey1)
	fooey2path = os.path.join(str(dir4), fooey2)

	# Verify these files are found
	temp_list = burger.traverse_directory(str(dir5), fooey1, False)
	assert temp_list == [fooey1path]

	temp_list = burger.traverse_directory(str(dir5), fooey2, False)
	assert temp_list == [fooey2path]

	# Perform tests that result in empty lists
	check_list = [fooey1path, fooey2path]
	temp_list = burger.traverse_directory(str(dir5), (fooey1, fooey2), False)
	assert temp_list == check_list
	temp_list = burger.traverse_directory(str(dir5), [fooey1, fooey2], False)
	assert temp_list == check_list
	temp_list = burger.traverse_directory(str(dir5), {fooey1, fooey2}, False)
	assert temp_list == check_list

	# Add some more files
	dir1.join(fooey1).write(fooey1)
	dir5.join(fooey2).write(fooey2)
	fooey1path2 = os.path.join(str(dir1), fooey1)
	fooey2path2 = os.path.join(str(dir5), fooey2)

	# Verify these files are found
	temp_list = burger.traverse_directory(str(dir5), fooey1, False)
	assert temp_list == [fooey1path2, fooey1path]

	temp_list = burger.traverse_directory(str(dir5), fooey2, False)
	assert temp_list == [fooey2path, fooey2path2]

	# Perform tests that result in empty lists
	check_list = [fooey1path2, fooey1path, fooey2path, fooey2path2]
	temp_list = burger.traverse_directory(str(dir5), (fooey1, fooey2), False)
	assert temp_list == check_list
	temp_list = burger.traverse_directory(str(dir5), [fooey1, fooey2], False)
	assert temp_list == check_list
	temp_list = burger.traverse_directory(str(dir5), {fooey1, fooey2}, False)
	assert temp_list == check_list

	# Cleanup
	tmpdir.remove()
