#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Burger string functions

Package that contains string manipulation functions
"""

## \package burger.string

from __future__ import absolute_import, print_function, unicode_literals

import string
from .buildutils import get_windows_host_type

########################################


try:
	# Test if basestring exists (Only in Python 2.x)
	basestring										# pylint: disable=W0104,basestring-builtin

	def is_string(item):
		"""
		Return True if input is a string object

		Test the input if it's either an instance of
		basestring in Python 2.x or str in Python 3.x

		Args:
			item: Object to test
		Returns:
			True if the object is a string instance, False if not.
		"""

		return isinstance(item, basestring)			# pylint: disable=basestring-builtin

except NameError:

	# Assume Python 3.0 or higher
	def is_string(item):
		"""
		Return True if input is a string object

		Test the input if it's either an instance of
		basestring in Python 2.x or str in Python 3.x

		Args:
			item: Object to test
		Returns:
			True if the object is a string instance, False if not.
		"""

		return isinstance(item, (str, bytes))

########################################


def convert_to_array(input_array):
	"""
	Convert a string to a string array (list)

	If the input is already a list, return the list as is.
	Otherwise, convert the string to a single entry list.
	If the input is None, return an empty list.

	Args:
		input_array: A list or string object
	Returns:
		A list object.
	"""

	# If empty, return an empty array
	if input_array is None:
		input_array = []
	elif not isinstance(input_array, list):
		# Convert a single entry into an array
		input_array = [input_array]
	return input_array

########################################


def TrueFalse(item):			# pylint: disable=C0103
	"""
	Convert the input into a boolean and return the string 'True' or 'False'

	If the input was a string of '0' or 'False' (Case insensitive comparision),
	this function will return 'False'. Empty dictionary, string or list objects,
	or the number zero will also return 'False'

	Args:
		item: Object to convert to a bool before converting into a string
	Returns:
		The string 'True' or 'False'
	See:
		truefalse() or TRUEFALSE()
	"""

	# Test if it's the string 'False'
	if is_string(item):
		if item == '0' or item.upper() == 'FALSE':
			return 'False'
	if bool(item):
		return 'True'
	return 'False'

########################################


def truefalse(item):
	"""
	Convert the input into a boolean and return the string 'true' or 'false'

	If the input was a string of '0' or 'False' (Case insensitive comparision),
	this function will return 'false'. Empty dictionary, string or list objects,
	or the number zero will also return 'false'

	Args:
		item: Object to convert to a bool before converting into a string
	Returns:
		The string 'true' or 'false'
	See:
		TRUEFALSE() or TrueFalse()
	"""

	# Test if it's the string 'False'
	if is_string(item):
		if item == '0' or item.upper() == 'FALSE':
			return 'false'
	if bool(item):
		return 'true'
	return 'false'

########################################


def TRUEFALSE(item):			# pylint: disable=C0103
	"""
	Convert the input into a boolean and return the string 'TRUE' or 'FALSE'

	If the input was a string of '0' or 'False' (Case insensitive comparision),
	this function will return 'FALSE'. Empty dictionary, string or list objects,
	or the number zero will also return 'FALSE'

	Args:
		item: Object to convert to a bool before converting into a string
	Returns:
		The string 'TRUE' or 'FALSE'
	See:
		truefalse() or TrueFalse()
	"""

	# Test if it's the string 'False'
	if is_string(item):
		if item == '0' or item.upper() == 'FALSE':
			return 'FALSE'
	if bool(item):
		return 'TRUE'
	return 'FALSE'

########################################


def convert_to_windows_slashes(path_name, force_ending_slash=False):
	"""
	Convert a filename from linux/mac to windows format

	Convert all '/' characters into '\' characters

	If force_ending_slash is True, append a '\' if one is not
	present in the final string

	Args:
		path_name: A pathname to be converted to Windows slashes
		force_ending_slash: True if a '\\' character is to be forced at the end
			of the output

	Returns:
		A pathname using Windows type slashes '\\'

	See:
		convert_to_linux_slashes()

	"""

	result = path_name.replace('/', '\\')
	if force_ending_slash and not result.endswith('\\'):
		result = result + '\\'
	return result

########################################


def convert_to_linux_slashes(path_name, force_ending_slash=False):
	"""
	Convert a filename from windows to linux/mac format

	Convert all '\' characters into '/' characters

	Args:
		path_name: A string object that text substitution will occur
		force_ending_slash: True if a '/' character is to be forced at the end
			of the output

	Returns:
		A pathname using Linux/BSD type slashes '/'

	See:
		convert_to_windows_slashes()
	"""

	result = path_name.replace('\\', '/')
	if force_ending_slash and not result.endswith('/'):
		result = result + '/'
	return result

########################################


_WINDOWSSAFESET = frozenset(string.ascii_letters + string.digits + '_-.:\\')
_LINUXSAFESET = frozenset(string.ascii_letters + string.digits + '@%_-+=:,./')


def encapsulate_path(input_path):

	"""
	Quote a pathname for use in the native system shell

	On windows platforms, if the path has a space or other
	character that could confuse COMMAND.COM, the string
	will be quoted, and for other platforms, it will
	be quoted using rules that work best for BASH.
	This will also quote if the path has a ';' which
	could be used to confuse bash.

	Args:
		input_path: string with the path to encapsulate
	Returns:
		Input string or input properly quoted
	"""

	# Process for Windows platforms
	if get_windows_host_type():

		# Force to windows slashes
		temp = convert_to_windows_slashes(input_path)

		# If there are illegal characters, break
		for item in temp:
			if item not in _WINDOWSSAFESET:
				break
		else:
			# String doesn't need quotes
			if not temp:
				return '""'
			return temp
		# Quote the string
		return '"{}"'.format(temp.replace('"', '^"'))

	# Force to linux slashes
	temp = convert_to_linux_slashes(input_path)

	# If there are illegal characters for linux/BSD, break
	for item in temp:
		if item not in _LINUXSAFESET:
			break
	else:
		# String doesn't need quotes
		if not temp:
			return "''"
		return temp
	# Enquote the string for Linux or MacOSX
	return "'{}'".format(temp.replace("'", "'\"'\"'"))
