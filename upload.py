#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Build and upload the egg file
#

# Copyright 2013-2015 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

import os
import sys
import burger
import argparse
import shutil

#
# Clean up all the temp files after uploading
# Helps in keeping source control from having to track
# temp files
#

def clean(workingDir):
	shutil.rmtree(os.path.join(workingDir,'burger.egg-info'),ignore_errors=True)
	shutil.rmtree(os.path.join(workingDir,'dist'),ignore_errors=True)
	shutil.rmtree(os.path.join(workingDir,'build'),ignore_errors=True)
	shutil.rmtree(os.path.join(workingDir,'temp'),ignore_errors=True)

	#
	# Delete all *.pyc and *.pyo files
	#
	
	nameList = os.listdir(workingDir)
	for baseName in nameList:
		fileName = os.path.join(workingDir,baseName)
		# Is it a file?
		if os.path.isfile(fileName):
			if baseName.endswith('.pyc') or baseName.endswith('.pyo') :
				os.remove(fileName)

#
# Upload the documentation to the server
#

def main(workingDir):

	
	# Parse the command line
	
	parser = argparse.ArgumentParser(
		description='Upload python distribution. Copyright by Rebecca Ann Heineman',
		usage='upload [-h] [-d]')
	parser.add_argument('-d','-dontclean', dest='dont_clean', action='store_true',
		default=False,
		help='Don\'t perform a clean after uploading')

	parser.add_argument('-c','-clean', dest='clean', action='store_true',
		default=False,
		help='Perform a clean and immediately exit.')

	args = parser.parse_args()

	#
	# Do a clean and exit
	#
	
	if args.clean==True:
		clean(workingDir)
		return 0
		
	#
	# Perform the upload
	#
	
	sys.argv = ['setup.py','sdist','upload']
	error = execfile('setup.py')
	if error != 0:
	
		#
		# Clean up afterwards
		#
		
		if args.dont_clean!=True:
			clean(workingDir)
	
	return error
		
# 
# If called as a function and not a class,
# call my main
#

if __name__ == "__main__":
	sys.exit(main(os.path.dirname(os.path.abspath(__file__))))
