#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A set of subroutines used by the Burgerlib based scripts written in Python.

Copyright 2013-2018 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

# Too many lines in module C0302 (Long file)
# pylint: disable=C0302

#
## \mainpage Burgerlib Python Index
#
# \par List of Classes
#
# \li \ref burger
# \li \ref burger.Node
# \li \ref burger.Interceptstdout
#
# To use the library:
# \code
#
# # Import the burger libary
# import burger
#
# \endcode
#
# To install type in 'pip install burger' from your shell.
#
# The source can be found at github at https://github.com/burgerbecky/pyburger
#
# Email becky@burgerbecky.com for comments, bugs or coding suggestions.
#

#
## \package burger
# A set of subroutines used by the Burgerlib based scripts
# written in Python.
#
# For higher level tools like makeprojects, cleanme and
# buildme, common subroutines were collected and
# placed in this module for reuse.
#

from __future__ import absolute_import, print_function, unicode_literals

import errno
import os
import platform
import shutil
import stat
import string
import subprocess
import sys

# Use the old way for Python 2 versus 3
_PY2 = sys.version_info[0] == 2
if _PY2:
	from cStringIO import StringIO
else:
	from io import StringIO

# Redefining built-in W0622 (Ignore redefinition of zip)

try:
	import itertools.izip as zip		# pylint: disable=W0622
except ImportError:
	pass

## Current version of the library
__version__ = '1.0.2'

## Author's name
__author__ = 'Rebecca Ann Heineman <becky@burgerbecky.com>'

## Name of the module
__title__ = 'burger'

## Summary of the module's use
__summary__ = 'Burger Becky\'s shared python library.'

## Home page
__uri__ = 'http://burgerbecky.com'

## Email address for bug reports
__email__ = 'becky@burgerbecky.com'

## Type of license used for distribution
__license__ = 'MIT License'

## Copyright owner
__copyright__ = 'Copyright 2013-2018 Rebecca Ann Heineman'

#
## Items to import on "from burger import *"
#

__all__ = [
	'Interceptstdout',
	'is_string',
	'get_sdks_folder',
	'create_folder_if_needed',
	'delete_file',
	'convert_to_array',
	'TrueFalse',
	'truefalse',
	'TRUEFALSE',
	'convert_to_windows_slashes',
	'convert_to_linux_slashes',
	'Node',
	'host_machine',
	'fix_csharp',
	'get_windows_host_type',
	'get_mac_host_type',
	'where_is_doxygen',
	'where_is_p4',
	'perforce_edit',
	'compare_files',
	'compare_file_to_string',
	'run_command',
	'make_version_header',
	'is_codewarrior_mac_allowed',
	'is_source_newer',
	'copy_file_if_needed',
	'copy_file_checkout_if_needed',
	'copy_directory_if_needed',
	'shutil_readonly_cb',
	'delete_directory',
	'get_tool_path',
	'traverse_directory',
	'encapsulate_path',
	'unlock_files',
	'lock_files'
]

########################################

class Interceptstdout(list):
	"""
	Handy class for capturing stdout from tools and	python itself

	Examples:
		# Import the class
		from burger import Interceptstdout

		# Instanciate the class, which intercepts stdout
		with Interceptstdout() as output:
			do_somethingthatprints()
			print('capture me!')

		# Once out of scope, output has a list of strings
		# of the captured stdout output.
		print(output)

	"""

	def __init__(self):
		"""
		Declares the internal variables
		"""

		## Saved copy of sys.stdout
		self._stdout = None

		## StringIO to redirect output to
		self._stringio = None
		super(Interceptstdout, self).__init__()

	def __enter__(self):
		"""
		Invoked on 'with' which intercepts all future stdout
		"""

		self._stdout = sys.stdout
		sys.stdout = self._stringio = StringIO()
		return self

	def __exit__(self, *args):
		"""
		Disconnect the stdout and store the items into a list of lines

		Using splitlines(), output the buffer into a list of lines
		into the output field
		"""

		# Restore stdout on exit
		self.extend(self._stringio.getvalue().splitlines())
		sys.stdout = self._stdout
		self._stringio = None
		self._stdout = None

########################################

try:
	# Test if basestring exists (Only in Python 2.x)
	basestring										#pylint: disable=W0104,basestring-builtin

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

		return isinstance(item, basestring)			#pylint: disable=basestring-builtin

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

		return isinstance(item, str)

########################################

def get_sdks_folder():
	"""
	Return the path of the BURGER_SDKS folder

	If the environment variable BURGER_SDKS is set,
	return the pathname it contains. Otherwise,
	print a warning and return None.

	Returns:
		None if the environment variable is not set, or the
		value of BURGER_SDKS.
	"""

	sdks = os.getenv('BURGER_SDKS')
	if sdks is None:
		print('The environment variable "BURGER_SDKS" is not set')
	return sdks

########################################

def create_folder_if_needed(path):
	"""
	Given a pathname to a folder, detect if the folder exists, if not, create it.

	Call os.makedirs(path) but does not throw an
	exception if the directory already exists.

	Args:
		path: A string object with the pathname.
	"""

	try:
		os.makedirs(path)
	except OSError as error:
		if error.errno != errno.EEXIST:
			raise

########################################

def delete_file(filename):
	"""
	Given a pathname to a file, delete it.

	If the file doesn't exist, it will return without raising
	an exception.

	Args:
		filename: A string object with the filename
	"""

	try:
		os.remove(filename)
	except OSError as error:
		if error.errno != errno.ENOENT:
			raise

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

def TrueFalse(item):			#pylint: disable=C0103
	"""
	Convert the input into a boolean and return the string 'True' or 'False'

	If the input was a string of '0' or 'False' (Case insensitive comparision),
	this function will return 'False'. Empty dictionary, string or list objects, or the number
	zero will also return 'False'

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
	this function will return 'false'. Empty dictionary, string or list objects, or the number
	zero will also return 'false'

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

def TRUEFALSE(item):			#pylint: disable=C0103
	"""
	Convert the input into a boolean and return the string 'TRUE' or 'FALSE'

	If the input was a string of '0' or 'False' (Case insensitive comparision),
	this function will return 'FALSE'. Empty dictionary, string or list objects, or the number
	zero will also return 'FALSE'

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
		force_ending_slash: True if a '\\' character is to be forced at the end of the output

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
		force_ending_slash: True if a '/' character is to be forced at the end of the output

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

class Node(object):
	"""
	Node class for creating directory trees

	Needed for some projects that have to store
	file entries in nested trees
	"""

	# Too few public methods R0903
	# #pylint: disable=R0903

	def __init__(self, value, children=None):
		"""
		Create a node with an initial value

		Args:
			value: Object to be the value of this node
			children: Array of nodes to be added as children to this one
		"""

		if children is None:
			children = []

		## Value contained in this node
		self.value = value
		## Array of children nodes to this node
		self.children = children

	def __repr__(self, level=0):
		"""
		Display this node as a string

		Args:
			level: Recursion depth (Used internally)
		"""

		ret = '\t'*level+repr(self.value)+'\n'
		for child in self.children:
			ret += child.__repr__(level+1)
		return ret

	__str__ = __repr__


########################################

def host_machine():
	"""
	Return the high level operating system's name

	Return the machine this script is running on, 'windows', 'macosx',
	'linux' or 'unknown'

	Returns:
		The string 'windows', 'macosx', 'linux', or 'unknown'

	See:
		get_mac_host_type() or get_windows_host_type()
	"""
	# Only windows reports as NT

	if os.name == 'nt':
		return 'windows'

	# BSD and GNU report as posix

	if os.name == 'posix':

		# MacOSX is the Darwin kernel

		if platform.system() == 'Darwin':
			return 'macosx'

		# Assume linux (Tested on Ubuntu and Red Hat)

		return 'linux'

	# Surrender Dorothy

	return 'unknown'

########################################

def fix_csharp(csharp_application_path):
	"""
	Convert pathname to execute a C# exe file

	C# applications can launch as is on Windows platforms,
	however, on Mac OSX and Linux, it must be launched
	from mono. Determine the host machine and if not
	windows, automatically prepend 'mono' to
	the application's name to properly launch it

	This will also encase the name in quotes in case there are
	spaces in the pathname

	Args:
		csharp_application_path: Pathname string to update

	Returns:
		Command line appropriate for the platform to launch a C# application.
	"""

	if host_machine() != 'windows':
		return 'mono "{}"'.format(csharp_application_path)
	return '"{}"'.format(csharp_application_path)


########################################

def get_windows_host_type():
	"""
	Return windows host type (32 or 64 bit)

	Return False if the host is not Windows, 'x86' if it's a 32 bit host
	and 'x64' if it's a 64 bit host, and possibly 'arm' if an arm host

	Returns:
		The string 'x64', 'x86', 'arm' or False
	See:
		get_mac_host_type() or host_machine()

	"""

	# Not windows?

	if os.name != 'nt':
		return False

	# Test the CPU for the type

	machine = platform.machine()
	if machine == 'AMD64':
		return 'x64'
	return 'x86'

########################################

def get_mac_host_type():
	"""
	Return Mac OSX host type (PowerPC/Intel)

	Return False if the host is not Mac OSX. 'ppc' if it's a Power PC based
	system, 'x86' for Intel (Both 32 and 64 bit)

	Returns:
		The string 'x86', 'ppc' or False

	See:
		get_windows_host_type() or host_machine()
	"""

	# Mac/Linux?
	if os.name != 'posix':
		return False

	# Not linux?

	if platform.system() != 'Darwin':
		return False

	# Since it's a mac, query the Mac OSX cpu type
	# using the MacOSX python extensions

	mac_ver = platform.mac_ver()
	cpu = mac_ver[2]
	if cpu == 'x86' or cpu == 'x86_64':
		return 'x86'

	if cpu == 'PowerPC':
		return 'ppc'

	# default to PowerPC
	return 'ppc'

########################################

def where_is_doxygen():
	"""
	Return the location of Doxygen's executable

	Look for an environment variable DOXYGEN and
	determine if the executable resides there, if
	so, return the string to the path

	If running on a MacOSX client, look in the Applications
	folder for a copy of Doxygen.app and return the
	pathname to the copy of doxygen that resides within

	If it cannot be determined that doxygen is installed,
	the string 'doxygen' is returned expecting
	that the executable is in the PATH

	Returns:
		A path to the Doxygen command line executable or None if not found.

	"""

	# Is Doxygen installed on windows?

	if get_windows_host_type() != False:

		# Try the environment variable

		doxygenpath = os.path.expandvars('${DOXYGEN}\\bin\\doxygen.exe')
		if doxygenpath != None:
			if not os.path.isfile(doxygenpath):
				doxygenpath = None

		# Try 64 bit version or native 32 bit version
		if doxygenpath is None:
			doxygenpath = os.path.expandvars('${ProgramFiles}\\doxygen\\bin\\doxygen.exe')
			if doxygenpath != None:
				if not os.path.isfile(doxygenpath):
					doxygenpath = None

		# Try 32 bit version on 64 bit system

			if doxygenpath is None:
				doxygenpath = os.path.expandvars('${ProgramFiles(x86)}\\doxygen\\bin\\doxygen.exe')
				if doxygenpath != None:
					if not os.path.isfile(doxygenpath):
						doxygenpath = None

			if doxygenpath is None:
				print('Doxygen needs to be installed to build documentation!')

		return doxygenpath

	# MacOSX has it hidden in the application
	elif get_mac_host_type() != False:
		doxygenpath = '/Applications/Doxygen.app/Contents/Resources/doxygen'
		if not os.path.isfile(doxygenpath):
			print('Doxygen needs to be installed in your Applications folder to build documentation!')
			return None
		return doxygenpath

	# None of the above
	return 'doxygen'

########################################

def expand_and_verify(file_string):
	"""
	Expand the input string with os.path.expandvars()

	After expanding the string, test for the existence of the file
	and return the expanded path if True. Otherwise, return None

	Examples:
		perforcepath = burger.expand_and_verify('${PERFORCE}\\p4.exe')
		if perforcepath is None:
			return

	Args:
		file_string: Pathname with environment variable tokens

	Returns:
		None if the string couldn't be expanded or if the file didn't exist,
			otherwise, return the expanded pathname

	"""

	result_path = os.path.expandvars(file_string)
	if result_path is not None:
		if not os.path.isfile(result_path):
			result_path = None
	return result_path

########################################

def where_is_p4(encapsulate=True):

	"""
	Return the location of the p4 executable

	Note: This returns the string in a format that is used
	to call p4 from a shell, so on Windows clients it may
	be encased in quotes to allow spaces in the full pathname

	If it cannot be determined that p4 is installed,
	the string 'p4' is returned expecting
	that the executable is in the PATH

	Args:
		encapsulate: If True, return the path enquoted, otherwise don't encapsulate in quotes.
	"""

	# Is Perforce installed on windows?

	if get_windows_host_type() != False:

		# Try the environment variable

		perforce_path = expand_and_verify('${PERFORCE}\\p4.exe')

		# Try 64 bit version or native 32 bit version
		if perforce_path is None:
			perforce_path = expand_and_verify('${ProgramFiles}\\Perforce\\p4.exe')

		# Try 32 bit version on 64 bit system

			if perforce_path is None:
				perforce_path = expand_and_verify('${ProgramFiles(x86)}\\Perforce\\p4.exe')
				if perforce_path is None:
					print('Perforce needs to be installed for source control!')
					return None

		if encapsulate:
			return '"{}"'.format(perforce_path)
		return perforce_path

	# Is the path set for Linux or Mac OSX?

	perforce_path = os.getenv('PERFORCE')
	if perforce_path != None:
		perforce_path = os.path.join(perforce_path, 'p4')
		if encapsulate:
			return '"{}"'.format(perforce_path)
		return perforce_path

	# Assume it's in the PATH on other systems
	return 'p4'

########################################

def perforce_edit(files):

	"""
	Given a list of files, checkout (Edit) them in perforce

	Pass either a single string or a string list of pathnames
	of files to checkout in perforce using the 'p4 edit' command

	Args:
		files: list or string object of file(s) to checkout

	Returns:
		Zero if no error, non-zero on error
	"""

	# Get the p4 executable
	perforce_path = where_is_p4()

	# Not found?
	if perforce_path is None:
		return 10

	if not isinstance(files, list):
		files = [files]

	for item in files:
		cmd = '{} edit "{}"'.format(perforce_path, os.path.abspath(item))
		error = subprocess.call(cmd, shell=True)
		if error != 0:
			return error
	return 0

########################################

def compare_files(filename1, filename2):
	"""
	Compare text files for equality

	Check if two text files are the same length,
	and then test the contents to verify equality.

	Args:
		filename1: string object with the pathname of the file to test
		filename2: string object with the pathname of the file to test against

	Returns:
		True if the files are equal, False if not.

	See:
		compare_file_to_string()
	"""

	# Load in the two text files

	try:
		with open(filename1, 'r') as filep:
			file_one_lines = filep.readlines()
		with open(filename2, 'r') as filep:
			file_two_lines = filep.readlines()
	except IOError as error:
		# Only deal with file not found
		if error.errno != errno.ENOENT:
			raise
		# If not found, return "not equal"
		return False

	del filep

	# Compare the file contents

	if len(file_one_lines) == len(file_two_lines):
		for i, j in zip(file_one_lines, file_two_lines):
			if i != j:
				break
		else:
			# It's a match!
			return True
	return False

########################################

def compare_file_to_string(filename, data):

	"""
	Compare text file and a string for equality

	Check if a text file is the same as a string by loading the text file and
	testing line by line to verify the equality of the contents

	Args:
		filename: string object with the pathname of the file to test
		data: string object to test against

	Returns:
		True if the file and the string are the same, False if not

	See:
		compare_files()
	"""

	# Do a data compare as a text file

	try:
		with open(filename, 'r') as filep:
			file_one_lines = filep.readlines()
	except IOError as error:
		# Only deal with file not found
		if error.errno != errno.ENOENT:
			raise
		# If not found, return "not equal"
		return False

	del filep

	# Compare the file contents taking into account
	# different line endings

	file_two_lines = data.splitlines(True)

	# Compare the file contents

	if len(file_one_lines) == len(file_two_lines):
		for i, j in zip(file_one_lines, file_two_lines):
			if i != j:
				break
		else:
			# It's a match!
			return True
	return False

########################################

def run_command(args, working_dir=None, quiet=False):
	"""
	Execute a program and capture the return code and text output

	Args:
		args: List of command line entries, starting with the program pathname
		working_dir: Directory to set before executing command
		quiet: Set to True if errors should not be printed

	Returns:
		The return code, stdout, stderr
	"""
	try:
		tempfp = subprocess.Popen(args, cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, \
			universal_newlines=True)
	except OSError as error:
		if not quiet:
			print('Command line "{}" generated {}'.format(args, error))
		return (error.errno, '', '')

	stdoutstr, stderrstr = tempfp.communicate()
	return (tempfp.returncode, stdoutstr, stderrstr)

########################################

def make_version_header(working_dir, outputfilename):
	"""
	Create a C header with the perforce version

	This function assumes version control is with perforce!

	Get the last change list and create a header
	with this information (Only modify the output file if
	the contents have changed)

	C++ defines are declared for P4_CHANGELIST, P4_CHANGEDATE, P4_CHANGETIME,
	P4_CLIENT, and P4_USER

	Args:
		working_dir: string with the path of the folder to obtain the perforce version for
		outputfilename: string with the path of the generated header

	Returns:
		Zero if no error, non-zero on error
	"""

	# Check if perforce is installed
	p4exe = where_is_p4()
	if p4exe is None:
		return 10

	# Create the header guard by taking the filename,
	# converting to upper case and replacing spaces and
	# periods with underbars.
	headerguard = os.path.basename(outputfilename).upper()
	headerguard = headerguard.replace(' ', '_')
	headerguard = '__{}__'.format(headerguard.replace('.', '_'))

	# Get the last change list
	# Parse "Change 3361 on 2012/05/15 13:20:12 by burgerbecky@burgeroctocore 'Made a p4 change'"
	# -m 1 / Limit to one entry
	# -t / Display the time
	# -l / Print out the entire changelist description

	error, tempdata = run_command("{} changes -m 1 -t -l ...#have".format(p4exe), working_dir)[:2]
	if error != 0:
		return error

	# Parse out the output of the p4 changes command
	p4changes = tempdata.strip().split(' ')

	# Get the p4 client
	# Parse "P4CLIENT=burgeroctocore (config)"

	error, tempdata = run_command("{} set P4CLIENT".format(p4exe), working_dir)[:2]
	if error != 0:
		return error

	# Parse out the P4CLIENT query
	p4clients = tempdata.strip().split(' ')[0].split('=')

	# Get the p4 user
	# Parse "P4USER=burgerbecky (config)"

	error, tempdata = run_command("{} set P4USER".format(p4exe), working_dir)[:2]
	if error != 0:
		return error

	# Parse out the P4USER query
	p4users = tempdata.strip().split(' ')[0].split('=')

	# Write out the header

	filep = StringIO()
	filep.write( \
		'/***************************************\n'
		'\n'
		'\tThis file was generated by a call to\n'
		'\tburger.make_version_header() from a build\n'
		'\tpython script\n'
		'\n'
		'***************************************/\n'
		'\n'
		'#ifndef {0}\n'
		'#define {0}\n'
		'\n'.format(headerguard))

	if len(p4changes) > 4:
		filep.write('#define P4_CHANGELIST ' + p4changes[1] + '\n')
		filep.write('#define P4_CHANGEDATE "' + p4changes[3] + '"\n')
		filep.write('#define P4_CHANGETIME "' + p4changes[4] + '"\n')

	if len(p4clients) > 1:
		filep.write('#define P4_CLIENT "' + p4clients[1] + '"\n')

	if len(p4users) > 1:
		filep.write('#define P4_USER "' + p4users[1] + '"\n')

	filep.write('\n#endif\n')

	# Check if the data is different than what's already stored on
	# the drive

	filevalue = filep.getvalue()
	del filep
	if compare_file_to_string(outputfilename, filevalue) != True:
		print('Writing ' + outputfilename)
		try:
			with open(outputfilename, 'w') as filep:
				filep.write(filevalue)
		except IOError as error:
			print(error)
			return 2

	return 0

########################################

def is_codewarrior_mac_allowed():
	"""
	Return True if this machine can run Codewarrior for Mac OS Carbon

	Test first if the host platform is a mac, and if so, test if it's
	capable of running Mac OS Carbon Codewarrior 9 or 10

	Returns:
		True if CodeWarrior for Mac OS can be run on this Macintosh

	See:
		host_machine()
	"""

	# Test if a mac

	if host_machine() == 'macosx':
		# Get the Mac OS version number
		mac_ver = platform.mac_ver()
		release = mac_ver[0]

		# Convert 10.5.8 to 10.5

		digits = release.split('.')

		# Snow Leopard (10.6) supports Rosetta
		# Lion (10.7) and Mountain Lion (10.8) do not

		if float(digits[0]) == 10:
			if float(digits[1]) < 7:
				return True

	# Can't run, not a mac or Power PC native or emulation isn't supported
	return False

########################################

def is_source_newer(source, destination):
	"""
	Return False if the source file is older then the destination file

	Check the modification times of both files to determine if the
	source file is newer

	Return False if destination is newer, not False if not.

	Args:
		source: string pathname of the file to test
		destination: string pathname of the file to test against

	Returns:
		False if not newer, True if newer, 2 if there is no source file
	"""

	# Get the source file's modification time, If there's no source file, return 2
	try:
		srctime = os.path.getmtime(source)
	except OSError as error:
		if error.errno != errno.ENOENT:
			raise
		return 2

	# Get the destination file's modification time, if missing return True
	try:
		desttime = os.path.getmtime(destination)
	except OSError as error:
		if error.errno != errno.ENOENT:
			raise
		return True

	# Is the source older or equal? Return False to not update the destination
	if srctime <= desttime:
		return False
	return True

########################################

def copy_file_if_needed(source, destination, silent=False):
	"""
	Copy a file only if newer

	Copy a file only if the destination is missing or is older than the source file

	Args:
		source: string pathname of the file to copy from
		destination: string pathname of the file to copy to
		silent: True if print output is suppressed

	Returns:
		Zero if no error otherwise non-zero
	"""

	# If there is a destination file, check the modification times

	if is_source_newer(source, destination) is True:

		# Copy the file

		if silent is not False:
			print('Copying {0} -> {1}'.format(source, destination))
		try:
			shutil.copyfile(source, destination)
		except IOError as error:
			print(error)
			return 2
	return 0

########################################

def copy_file_checkout_if_needed(source, destination, silent=False):

	"""
	Copy a file only if newer and alert Perforce if present

	Copy a file only if needed and check out the destination file before the copy
	operation if Perforce is detected

	Args:
		source: string pathname of the file to copy from
		destination: string pathname of the file to copy to
		silent: True if print output is suppressed

	Returns:
		Zero on no error, non-zero on error

	See:
		perforce_edit()
	"""

	if is_source_newer(source, destination) is True:

		# Alert perforce that the file is to be modified

		perforce_edit(destination)

		# Copy the file
		if silent is not False:
			print('Copying {} -> {}'.format(source, destination))
		try:
			shutil.copyfile(source, destination)
		except IOError as error:
			print(error)
			return 2
	return 0

########################################

def copy_directory_if_needed(source, destination, exception_list=None, silent=False):

	"""
	Copy all of the files in a directory into a new directory

	Creating any necessary directories in the process, and it
	will skip files with specific extensions

	Note:
		This is a recursive function

	Args:
		source: string pathname of the directory to copy from
		destination: string pathname of the directory to copy to
		exception_list: optional list of file extensions to ignore during copy
		silent: True if print output is suppressed

	Returns:
		Zero if no error, non-zero on error

	See:
		copy_file_if_needed(), create_folder_if_needed()
	"""

	# Ensure there is an exception list, even if empty
	if exception_list is None:
		exception_list = []

	# Make sure the output folder exists
	create_folder_if_needed(destination)

	name_list = os.listdir(source)
	for base_name in name_list:
		for item in exception_list:
			if base_name.endswith(item):
				break
		else:
			file_name = os.path.join(source, base_name)

			# Handle the directories found
			if os.path.isdir(file_name):
				# Recursive!
				error = copy_directory_if_needed(file_name, os.path.join(destination, base_name), \
					exception_list, silent)
			else:
				error = copy_file_if_needed(file_name, os.path.join(destination, base_name), silent)

			# Exit immediately on error
			if error != 0:
				return error

	return 0

########################################

def shutil_readonly_cb(func, path, exception_info):

	"""
	Subroutine for shutil.rmtree() to delete read only files

	shutil.rmtree() raises an exception if there are read
	only files in the directory being deleted. Use this
	callback to allow read only files to be disposed of.

	Examples:
		import burger
		import shutil

		shutil.rmtree(PATH_TO_DIRECTORY,onerror = burger.shutil_readonly_cb)

	Note:
		This is a callback function

	Args:
		func: Not used
		path: pathname of the file that is read only
		exception_info: Information about the exception

	See:
		delete_directory()
	"""

	# File not found? Ignore
	value = exception_info[1]
	if value.args[0] == errno.ENOENT:
		return

	# Read only?
	# EACCESS for Linux/MacOSX, EIO for Windows

	if value.args[0] == errno.EACCES or value.args[0] == errno.EIO:

		# Mark as writable and try again to delete the file
		os.chmod(path, stat.S_IWRITE)
		os.unlink(path)

########################################

def delete_directory(path, delete_read_only=False):
	"""
	Recursively delete a directory

	Delete a directory and all of the files and directories within.

	Args:
		path: Pathname of the directory to delete
		delete_read_only: True if read only files are to be deleted as well

	See:
		shutil_readonly_cb()
	"""

	if delete_read_only is False:
		shutil.rmtree(path, ignore_errors=True)
	else:
		shutil.rmtree(path, onerror=shutil_readonly_cb)

########################################

def get_tool_path(tool_folder, tool_name, encapsulate=False):

	"""
	Find executable tool directory

	For allowing builds on multiple operating system hosts under the Burgerlib
	way of project management, it's necessary to query what is the host operating system
	and glean out which folder to find a executable compiled for that specific host

	Args:
		tool_folder: Pathname to the folder that contains the executables
		tool_name: Bare name of the tool (Windows will append '.exe')
		encapsulate: False if a path is requested, True if it's quoted to be used as a
			string to be sent to command line shell

	Returns:
		Full pathname to the tool to execute
	"""

	host = host_machine()

	# Macosx uses fat binaries
	if host == 'macosx':
		exename = os.path.join(tool_folder, 'macosx', tool_name)

	# Linux is currently just 64 bit Intel, will have to update
	# as more platforms are supported
	elif host == 'linux':
		exename = os.path.join(tool_folder, 'linux', tool_name)

	# Windows supports 32 and 64 bit Intel
	elif host == 'windows':
		exename = os.path.join(tool_folder, 'windows', get_windows_host_type(), tool_name + '.exe')
	else:

	# On unknown platforms, assume the tool is in the path for the fallback
		exename = tool_name

	# Encase in quotes to handle spaces in filenames

	if encapsulate is True:
		return '"{}"'.format(exename)
	return exename

########################################

def traverse_directory(working_dir, filename):

	"""
	Create a list of all copies of a file following a directory

	Starting with a working directory, test if a file exists
	and if so, insert it into a list. The list will be
	starting from the root with the last entry
	being at the working directory

	Args:
		working_dir: string with the path of the folder to start the search
		filename: string with the name of the file to find in the folder

	Returns:
		List of pathnames (With filename appended)
	"""

	# Convert into a unpacked pathname
	tempdir = os.path.abspath(working_dir)
	dirlist = []

	# Loop
	while 1:
		# Is the file here?
		temppath = os.path.join(tempdir, filename)
		if os.path.isfile(temppath):
			# Insert at the beginning
			dirlist.insert(0, temppath)
		# Pop a folder
		tempdir2 = os.path.dirname(tempdir)
		# Already at the top of the directory?
		if tempdir2 is None or tempdir2 == tempdir:
			break
		# Use the new folder
		tempdir = tempdir2

	# Return the list of files
	return dirlist

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

########################################

def unlock_files(working_dir, recursive=False):
	"""
	Iterate over a directory and unlock all read-only files.

	This function will generate a list of fully qualified pathnames
	of every file that was unlocked. Directories will be skipped.

	Examples:
		# Any file that is read only in this directory is now unlocked
		lock_list = unlock_files("~/projects/lockedfiles")

		# Do stuff on the files
		do_code_on_unlocked_files()

		# Re-lock all the files that were unlocked.
		lock_files(lock_list)

	Args:
		working_dir: Pathname to the directory to traverse for read-only files
		recursive: False (default) don't recurse through folders, True, recurse
	Returns:
		A list object with the name of every file that was unlocked.

	See:
		lock_files()

	"""

	# Ensure the pathname is unmangled
	abs_dir = os.path.abspath(working_dir)

	# Iterate over the directory
	result = []
	for item in os.listdir(abs_dir):
		path_name = os.path.join(abs_dir, item)

		# Only process files, skip directories
		if os.path.isfile(path_name):
			if not os.access(path_name, os.W_OK):
				os.chmod(path_name, stat.S_IWRITE)
				result.append(path_name)
		else:
			if recursive and os.path.isdir(path_name):
				result += unlock_files(path_name, True)
	return result


########################################

def lock_files(lock_list):
	"""
	Iterate over the input list and mark all files as read-only

	Args:
		lock_list: Iterable object containing a list of path names to files
			or directories to mark as "read-only"
	See:
		unlock_files()
	"""
	for item in lock_list:
		os.chmod(item, stat.S_IREAD)
