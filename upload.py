#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Build and upload the egg file

Copyright 2013-2018 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

from __future__ import absolute_import, print_function, unicode_literals
import os
import sys
import argparse
import burger

#pylint: disable=W0122

########################################

def clean(working_dir):
	"""
	Clean up all the temp files after uploading

	Helps in keeping source control from having to track
	temp files
	"""

	# pylint: disable=C0330
	dirlist = [
		'burger.egg-info',
		'burger-' + burger.__version__,
		'dist',
		'build',
		'temp',
		'_build',
		'__pycache__'
	]

	# Delete all folders, including read only files

	for item in dirlist:
		burger.delete_directory(os.path.join(working_dir, item), True)

	#
	# Delete all *.pyc and *.pyo files
	#

	extension_list = [
		'.pyc',
		'.pyo'
	]

	name_list = os.listdir(working_dir)
	for base_name in name_list:
		file_name = os.path.join(working_dir, base_name)
		# Is it a file? (Skip directories)
		if os.path.isfile(file_name):
			for item in extension_list:
				if base_name.endswith(item):
					os.remove(file_name)
					break

########################################

def main(working_dir):
	"""
	Upload the documentation to the server
	"""

	# Parse the command line

	parser = argparse.ArgumentParser( \
		description='Build and upload a python distribution. Copyright by Rebecca Ann Heineman',
		usage='upload [-h] [-u] [-c]')

	parser.add_argument('-c', '-clean', dest='clean', action='store_true', \
		default=False, help='Perform a clean.')

	parser.add_argument('-u', '-upload', dest='upload', action='store_true', \
		default=False, help='Perform a full build and upload to https://pypi.python.org.')

	args = parser.parse_args()

	error = 0

	#
	# Perform the upload
	#

	lock_list = []

	try:
		if args.upload:
			lock_list = burger.unlock_files(working_dir)
			sys.argv = ['setup.py', 'sdist', 'upload']
			exec(open('setup.py').read())

		else:
			if not args.clean:
				lock_list = burger.unlock_files(working_dir)
				sys.argv = ['setup.py', 'build', 'sdist']
				exec(open('setup.py').read())

		#
		# Do a clean and exit
		#

		if args.clean:
			clean(working_dir)
			error = 0

	finally:
		burger.lock_files(lock_list)
	return error

########################################

# If called as a function and not a class, call my main

if __name__ == "__main__":
	sys.exit(main(os.path.dirname(os.path.abspath(__file__))))
