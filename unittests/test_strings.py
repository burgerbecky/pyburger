#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger string functions

Copyright 2013-2018 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

import sys
import burger

_PY2 = sys.version_info[0] == 2

########################################


def test_truefalse():
	"""
	Test burger.truefalse()
	"""

	assert burger.truefalse(0) == 'false'
	assert burger.truefalse(0.0) == 'false'
	assert burger.truefalse('0') == 'false'
	assert burger.truefalse('FALSE') == 'false'
	assert burger.truefalse('false') == 'false'
	assert burger.truefalse('False') == 'false'
	assert burger.truefalse(False) == 'false'
	assert burger.truefalse([]) == 'false'
	assert burger.truefalse({}) == 'false'
	assert burger.truefalse(()) == 'false'

	assert burger.truefalse(1) == 'true'
	assert burger.truefalse(1.0) == 'true'
	assert burger.truefalse('1') == 'true'
	assert burger.truefalse('TRUE') == 'true'
	assert burger.truefalse('true') == 'true'
	assert burger.truefalse('True') == 'true'
	assert burger.truefalse(True) == 'true'
	assert burger.truefalse([1]) == 'true'
	assert burger.truefalse({1}) == 'true'
	assert burger.truefalse((1)) == 'true'

	assert burger.truefalse('testing') == 'true'

########################################


def test_TRUEFALSE():		# pylint: disable=C0103
	"""
	Test burger.TRUEFALSE()
	"""

	assert burger.TRUEFALSE(0) == 'FALSE'
	assert burger.TRUEFALSE(0.0) == 'FALSE'
	assert burger.TRUEFALSE('0') == 'FALSE'
	assert burger.TRUEFALSE('FALSE') == 'FALSE'
	assert burger.TRUEFALSE('false') == 'FALSE'
	assert burger.TRUEFALSE('False') == 'FALSE'
	assert burger.TRUEFALSE(False) == 'FALSE'
	assert burger.TRUEFALSE([]) == 'FALSE'
	assert burger.TRUEFALSE({}) == 'FALSE'
	assert burger.TRUEFALSE(()) == 'FALSE'

	assert burger.TRUEFALSE(1) == 'TRUE'
	assert burger.TRUEFALSE(1.0) == 'TRUE'
	assert burger.TRUEFALSE('1') == 'TRUE'
	assert burger.TRUEFALSE('TRUE') == 'TRUE'
	assert burger.TRUEFALSE('true') == 'TRUE'
	assert burger.TRUEFALSE('True') == 'TRUE'
	assert burger.TRUEFALSE(True) == 'TRUE'
	assert burger.TRUEFALSE([1]) == 'TRUE'
	assert burger.TRUEFALSE({1}) == 'TRUE'
	assert burger.TRUEFALSE((1)) == 'TRUE'

	assert burger.TRUEFALSE('testing') == 'TRUE'

########################################


def test_TrueFalse():			# pylint: disable=C0103
	"""
	Test burger.TrueFalse()
	"""

	assert burger.TrueFalse(0) == 'False'
	assert burger.TrueFalse(0.0) == 'False'
	assert burger.TrueFalse('0') == 'False'
	assert burger.TrueFalse('FALSE') == 'False'
	assert burger.TrueFalse('false') == 'False'
	assert burger.TrueFalse('False') == 'False'
	assert burger.TrueFalse(False) == 'False'
	assert burger.TrueFalse([]) == 'False'
	assert burger.TrueFalse({}) == 'False'
	assert burger.TrueFalse(()) == 'False'

	assert burger.TrueFalse(1) == 'True'
	assert burger.TrueFalse(1.0) == 'True'
	assert burger.TrueFalse('1') == 'True'
	assert burger.TrueFalse('TRUE') == 'True'
	assert burger.TrueFalse('true') == 'True'
	assert burger.TrueFalse('True') == 'True'
	assert burger.TrueFalse(True) == 'True'
	assert burger.TrueFalse([1]) == 'True'
	assert burger.TrueFalse({1}) == 'True'
	assert burger.TrueFalse((1)) == 'True'

	assert burger.TrueFalse('testing') == 'True'

########################################


def test_isstring():
	"""
	Test burger.is_string()
	"""

	# Must return False
	assert not burger.is_string(0)
	assert not burger.is_string(None)
	assert not burger.is_string(True)
	assert not burger.is_string(False)
	assert not burger.is_string(1.0)
	assert not burger.is_string(())
	assert not burger.is_string({})
	assert not burger.is_string([])
	assert not burger.is_string(bytearray())
	assert not burger.is_string(bytearray(b'abc'))

	# Actual strings
	assert burger.is_string('a')
	assert burger.is_string(u'a')
	assert burger.is_string(b'a')
	assert burger.is_string(str('a'))
	assert burger.is_string('abc')
	assert burger.is_string(u'abc')
	assert burger.is_string(b'abc')
	assert burger.is_string(str('abc'))

	# Python 2.x tests (Not supported on 3.x or higher)
	if _PY2:
		assert burger.is_string(unicode('a'))
		assert burger.is_string(unicode(u'a'))
		assert burger.is_string(unicode(b'a'))
		assert burger.is_string(unicode('abc'))
		assert burger.is_string(unicode(u'abc'))
		assert burger.is_string(unicode(b'abc'))

	# Bytes need specific encoding passed in for Python 3.0 or higher
	if _PY2:
		assert burger.is_string(bytes('a'))
		assert burger.is_string(bytes(u'a'))
	else:
		assert burger.is_string(bytes('a', 'ascii'))
		assert burger.is_string(bytes(u'a', 'utf-8'))
	assert burger.is_string(bytes(b'a'))

	if _PY2:
		assert burger.is_string(bytes('abc'))
		assert burger.is_string(bytes(u'abc'))
	else:
		assert burger.is_string(bytes('abc', 'ascii'))
		assert burger.is_string(bytes(u'abc', 'utf-8'))
	assert burger.is_string(bytes(b'abc'))

	# False if it's a group of strings
	assert not burger.is_string(('a',))
	assert not burger.is_string(['a'])
	assert not burger.is_string({'a'})
	assert not burger.is_string(('a', 'b'))
	assert not burger.is_string(['a', 'b'])
	assert not burger.is_string({'a', 'b'})
