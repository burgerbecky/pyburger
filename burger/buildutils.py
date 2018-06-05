#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains build helper functions
"""

## \package burger.buildutils

from __future__ import absolute_import, print_function, unicode_literals

import errno
import os
import platform
import subprocess
import sys
from .strutils import is_string

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

## Cached location of the BURGER_SDKS folder
__BURGER_SDKS_FOLDER = None

## Cached location of doxygen
__DOXYGEN_PATH = None

## Cached location of p4 from Perforce
__PERFORCE_PATH = None

########################################


def get_sdks_folder(verbose=False, refresh=False, folder=None):
	"""
	Return the path of the BURGER_SDKS folder

	If the environment variable BURGER_SDKS is set,
	return the pathname it contains. Otherwise,
	print a warning if verbose is True and then attempt to find
	the 'sdks' folder by traversing the current working directory
	for a folder named 'sdks'. If one isn't found, return None.

	Examples:
		# Normal use
		sdksfolder = burger.buildutils.get_sdks_folder()
		if not sdksfolder:
			print('failure')
			raise NameError("sdks not found, set BURGER_SDKS")

		# Alert the user if BURGER_SDKS isn't set
		burger.buildutils.get_sdks_folder(verbose=True)

		# Force the use of a supplied folder for sdks
		burger.buildutils.get_sdks_folder(refresh=True, folder='./foo/sdks/')

	Args:
		verbose: If True, print a message if BURGER_SDKS was not present
		refresh: If True, reset the cache and force a reload.
		folder: Path to use as BURGER_SDKS in the cache as an override

	Returns:
		None if the environment variable is not set, or the
		value of BURGER_SDKS.
	"""

	global __BURGER_SDKS_FOLDER				# pylint: disable=W0603

	# Clear the cache if needed
	if refresh:
		__BURGER_SDKS_FOLDER = None

	# Set the override, if found
	if folder:
		__BURGER_SDKS_FOLDER = folder

	# Not cached?
	if __BURGER_SDKS_FOLDER is None:

		# Load from the system
		__BURGER_SDKS_FOLDER = os.getenv('BURGER_SDKS', default=None)

		# Test for None or empty string
		if not __BURGER_SDKS_FOLDER:

			# Warn about missing environment variable
			if verbose:
				print('The environment variable "BURGER_SDKS" is not set')

			# Try to find the directory in the current path
			from .fileutils import traverse_directory
			sdks = traverse_directory(os.getcwd(), 'sdks', \
				find_directory=True, terminate=True)
			if sdks:
				__BURGER_SDKS_FOLDER = sdks[0]
				if verbose:
					print('Assuming {} is the BURGER_SDKS folder'.format(sdks[0]))

	return __BURGER_SDKS_FOLDER

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

	# Encapsulate in quotes if needed
	from .strutils import encapsulate_path
	quoted = encapsulate_path(csharp_application_path)

	# Prepend mono on non-windows systems
	if host_machine() != 'windows':
		return 'mono {}'.format(quoted)
	return quoted


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
	if machine in ('AMD64', 'x86_64'):
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

	cpu = platform.machine()
	if cpu in ('x86', 'x86_64'):
		return 'x86'

	if cpu in ('PowerPC', 'ppc', 'Power Macintosh'):
		return 'ppc'

	# Defaults to PowerPC
	return 'ppc'

########################################


def is_exe(filename):
	"""
	Return True if the file is executable

	Note:
		Windows platforms don't support the 'x' bit so all
		files are executable if they exist.

	Args:
		filename: Full or partial pathname to test for existance
	Returns:
		True if the file is executable, False if the file doesn't exist or
		is not valid.
	"""
	return os.path.isfile(filename) and os.access(filename, os.X_OK)

########################################


def find_in_path(filename, search_path=None, executable=False):
	"""
	Using the system PATH environment variable, search for a file

	Args:
		filename: File to locate
		search_path: Search paths to use instead of PATH
		executable: True to ensure it's an executable
	Return:
		None if not found, a full path if the file is found
	"""

	# Is there a search path override?
	if search_path is None:
		# Use the environment variable
		search_path = os.getenv('PATH', None)

	# Is the search path a single string?
	if is_string(search_path):
		# Break it up based on the path seperator
		paths = search_path.split(os.pathsep)
	else:
		# Assume it's a tuple/list/dict of strings
		paths = search_path

	# Scan the list of paths to find the file
	for item in paths:
		# Try as is
		temp_path = os.path.join(item, filename)
		if os.path.isfile(temp_path):
			# Check if executable
			if not executable or os.access(temp_path, os.X_OK):
				break
	else:
		return os.path.abspath(temp_path)

	# Not found
	return None

########################################


def where_is_doxygen(verbose=False, refresh=False, path=None):
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

	Args:
		verbose: If True, print a message if doxygen was not found
		refresh: If True, reset the cache and force a reload.
		path: Path to doxygen to place in the cache

	Returns:
		A path to the Doxygen command line executable or None if not found.

	"""

	global __DOXYGEN_PATH				# pylint: disable=W0603

	# Clear the cache if needed
	if refresh:
		__DOXYGEN_PATH = None

	# Set the override, if found
	if path:
		__DOXYGEN_PATH = path

	# Is cached?
	if __DOXYGEN_PATH:
		return __DOXYGEN_PATH

	# Is Doxygen installed on windows?
	if get_windows_host_type():

		# Try the environment variable
		if os.getenv('DOXYGEN', None):
			doxygenpath = os.path.expandvars('${DOXYGEN}\\bin\\doxygen.exe')
			if os.path.isfile(doxygenpath):
				__DOXYGEN_PATH = doxygenpath
				return doxygenpath

		# Try 64 bit version or native 32 bit version
		if os.getenv('ProgramFiles', None):
			doxygenpath = os.path.expandvars( \
				'${ProgramFiles}\\doxygen\\bin\\doxygen.exe')
			if os.path.isfile(doxygenpath):
				__DOXYGEN_PATH = doxygenpath
				return doxygenpath

		# Try 32 bit version on 64 bit system
		if os.getenv('ProgramFiles(x86)', None):
			doxygenpath = os.path.expandvars( \
				'${ProgramFiles(x86)}\\doxygen\\bin\\doxygen.exe')
			if os.path.isfile(doxygenpath):
				__DOXYGEN_PATH = doxygenpath
				return doxygenpath

		if verbose:
			print('Doxygen not found!')
		return None

	# MacOSX has it hidden in the application
	elif get_mac_host_type():
		# Try the hidden file in the application first
		doxygenpath = '/Applications/Doxygen.app/Contents/Resources/doxygen'
		if os.path.isfile(doxygenpath):
			__DOXYGEN_PATH = doxygenpath
			return doxygenpath

		# Try macports
		doxygenpath = '/opt/local/bin/doxygen'
		if os.path.isfile(doxygenpath):
			__DOXYGEN_PATH = doxygenpath
			return doxygenpath

		if verbose:
			print( \
				'Doxygen needs to be installed in your Applications folder '
				'to build documentation!')

	# Return the cache value
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
		encapsulate: If True, return the path enquoted, otherwise don't
			encapsulate in quotes.
	"""

	# Is Perforce installed on windows?

	if get_windows_host_type() is not False:

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
	if perforce_path is not None:
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
			file_one_lines = filep.read().splitlines()
		with open(filename2, 'r') as filep:
			file_two_lines = filep.read().splitlines()
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
			file_one_lines = filep.read().splitlines()
	except IOError as error:
		# Only deal with file not found
		if error.errno != errno.ENOENT:
			raise
		# If not found, return "not equal"
		return False

	del filep

	# Compare the file contents taking into account
	# different line endings

	# Test if this is a StringIO object
	if hasattr(data, 'getvalue'):
		file_two_lines = data.getvalue().splitlines()
	else:
		file_two_lines = data.splitlines()

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
		tempfp = subprocess.Popen(args, cwd=working_dir, stdout=subprocess.PIPE, \
			stderr=subprocess.PIPE, universal_newlines=True)
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
		working_dir: string with the path of the folder to obtain the perforce
			version for
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
	# Parse "Change 3361 on 2012/05/15 13:20:12 by burgerbecky@burgeroctocore
	# 'Made a p4 change'"
	# -m 1 / Limit to one entry
	# -t / Display the time
	# -l / Print out the entire changelist description

	error, tempdata = run_command( \
		"{} changes -m 1 -t -l ...#have".format(p4exe),
		working_dir)[:2]
	if error != 0:
		return error

	# Parse out the output of the p4 changes command
	p4changes = tempdata.strip().split(' ')

	# Get the p4 client
	# Parse "P4CLIENT=burgeroctocore (config)"

	error, tempdata = \
		run_command("{} set P4CLIENT".format(p4exe), working_dir)[:2]
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
	if compare_file_to_string(outputfilename, filevalue) is not True:
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
