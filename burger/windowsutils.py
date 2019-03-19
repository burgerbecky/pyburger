#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains windows only functions
"""

## \package burger.windowsutils

from __future__ import absolute_import, print_function, unicode_literals

from ctypes import c_wchar_p, create_string_buffer, c_uint, \
	string_at, wstring_at, byref, c_void_p
import array
from .strutils import get_windows_host_type

########################################


def get_file_info(filename, info):
	r"""
	Extract information from a windows exe file version resource.

	Given a windows exe file, extract the 'StringFileInfo' resource and
	parse out the data chunk named by info.

	Full list of resource names:
		https://docs.microsoft.com/en-us/windows/desktop/menurc/stringfileinfo-block

	Examples:
		file_version = burger.get_file_info('devenv.exe', 'FileVersion')
		product_version =  burger.get_file_info('devenv.exe', 'ProductVersion')

	Note:
		This function will always return None on non-windows platforms.

	Args:
		filename: Name of the windows file.
		info: Name of the data chunk to retrieve

	Return:
		None if no record found, or a valid string
	"""

	# Test if running on a windows host
	if get_windows_host_type():

		# Only import on windows hosts
		from ctypes import windll

		# Ensure it's unicode
		wchar_filename = c_wchar_p(filename)

		# Call windows to get the data size
		size = windll.version.GetFileVersionInfoSizeW(wchar_filename, None)

		# Was there no data to return?
		if size:

			# Create buffer for resource data
			res_data = create_string_buffer(size)

			# Extract the file data
			windll.version.GetFileVersionInfoW(wchar_filename, None, size, res_data)

			# Find the default codepage (Not everything is in English)
			record = c_void_p()
			length = c_uint()
			windll.version.VerQueryValueW(res_data, '\\VarFileInfo\\Translation', \
				byref(record), byref(length))
			# Was a codepage found?
			if length.value:

				# Parse out the first found codepage (It's the default language)
				# it's in the form of two 16 bit shorts
				codepages = array.array('H', string_at(record.value, length.value))

				# Extract information from the version using unicode and
				# the proper codepage
				windll.version.VerQueryValueW(res_data, \
					'\\StringFileInfo\\{0:04x}{1:04x}\\{2}'.format(codepages[0], \
					codepages[1], info), \
					byref(record), byref(length))
				# Return the final result removing the terminating zero
				return wstring_at(record.value, length.value - 1)
	return None
