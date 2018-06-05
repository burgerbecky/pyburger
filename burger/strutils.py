#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains string manipulation functions

"""

## \package burger.strutils

from __future__ import absolute_import, print_function, unicode_literals

import sys
import os
import string

########################################


def unicode_print(input_string):
	"""
	Handle printing a unicode string to stdout

	On some platforms, printing a unicode string will trigger
	a UnicodeEncodeError exception. In these cases, handle the
	exception and recode the string to the native string
	encoding.

	Args:
		input_string: A unicode string to print to stdout.
	"""

	# Print the string, if no exception, exit
	try:
		print(input_string)
	except UnicodeEncodeError:
		# Ensure it's encoded to utf-8
		encoded = input_string.encode('utf-8')
		if sys.version_info[0] == 2:

			# Python 2.x only accepts this as input
			print(encoded)
		else:

			# Python 3.x and higher will allow remapping to
			# selected character encoding
			print(encoded.decode(sys.stdout.encoding))

########################################


try:
	# Test if basestring exists (Only in Python 2.x)
	basestring										# pylint: disable=W0104,basestring-builtin
	_IS_STRING_TEST = basestring					# pylint: disable=C0103,basestring-builtin

except NameError:
	# Python 3 or later
	_IS_STRING_TEST = (str, bytes)


def is_string(item):
	"""
	Return True if input is a string object

	Test the input if it's either an instance of
	basestring in Python 2.x or (str, bytes) in Python 3.x

	Args:
		item: Object to test
	Returns:
		True if the object is a string instance, False if not.
	"""

	return isinstance(item, _IS_STRING_TEST)

########################################


def convert_to_array(input_array):
	"""
	Convert a string to a string array (list)

	If the input is None, return an empty list. If
	it's a string, convert the string to a single entry list.
	Otherwise, assume it's an iterable dir, list or tuple of
	strings.

	Args:
		input_array: The object to test
	Returns:
		The input, or a string encapsulated into a single entry list.

	"""

	# If empty, return an empty array
	if input_array is None:
		input_array = []
	elif is_string(input_array):
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
	Convert a filename from Linux/macOS to Windows format

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
	Convert a filename from Windows to Linux/macOS format

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


def encapsulate_path_windows(input_path):

	"""
	Quote a pathname for use in the Windows system shell

	On Windows platforms, if the path has a space or other
	character that could confuse COMMAND.COM, the string
	will be quoted and double quotes within the string handled
	properly. All slash characters will be replaced with backslash
	characters.

	Args:
		input_path: string with the path to encapsulate using Windows rules
	Returns:
		Original input string if Windows can accept it or input properly quoted
	See:
		encapsulate_path()
	"""

	# Force to Windows slashes
	temp = convert_to_windows_slashes(input_path)

	# If there are any illegal characters, break
	for item in temp:
		if item not in _WINDOWSSAFESET:
			break
	else:
		# No illegal characters in the string
		if not temp:
			return '""'
		return temp

	# Since the test failed, quote the string
	return '"{}"'.format(temp.replace('"', '\\"'))

########################################


_LINUXSAFESET = frozenset(string.ascii_letters + string.digits + '@%_-+=:,./')


def encapsulate_path_linux(input_path):
	"""
	Quote a pathname for use in the linux or BSD system shell

	On Linux platforms, if the path has a space or other
	character that could confuse bash, the string
	will be quoted and double quotes within the string handled
	properly. All backslash characters will be replaced with slash
	characters.

	Args:
		input_path: string with the path to encapsulate using Windows rules
	Returns:
		Original input string if Windows can accept it or input properly quoted
	See:
		encapsulate_path()
	"""

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

########################################


def encapsulate_path(input_path):

	"""
	Quote a pathname for use in the native system shell

	On Windows platforms, if the path has a space or other
	character that could confuse COMMAND.COM, the string
	will be quoted, and for other platforms, it will
	be quoted using rules that work best for BASH.
	This will also quote if the path has a ';' which
	could be used to confuse bash.

	Args:
		input_path: string with the path to encapsulate
	Returns:
		Input string or input properly quoted
	See:
		encapsulate_path_windows() and encapsulate_path_linux()
	"""

	# Process for Windows platforms
	if os.name == 'nt':
		return encapsulate_path_windows(input_path)

	# Force to linux slashes
	return encapsulate_path_linux(input_path)
