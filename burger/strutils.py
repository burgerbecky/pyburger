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
import re
import csv
import fnmatch
import platform

## True if the interpreter is Python 2.x
PY2 = sys.version_info[0] == 2

## True if the interpreter is Python 3.x or higher
PY3_OR_HIGHER = sys.version_info[0] >= 3

## True if the interpreter is Python 3.3 or higher
PY3_3_OR_HIGHER = sys.version_info >= (3, 3, 0)

## True if the interpreter is Python 3.4 or higher
PY3_4_OR_HIGHER = sys.version_info >= (3, 4, 0)

## True if the interpreter is Python 3.5 or higher
PY3_5_OR_HIGHER = sys.version_info >= (3, 5, 0)

## True if the interpreter is PyPy
PYPY = platform.python_implementation() == 'PyPy'

## Valid characters for windows filenames without quoting
_WINDOWSSAFESET = frozenset(string.ascii_letters + string.digits + '_-.:\\')

## Valid characters for macOS and Linux files without quoting
_LINUXSAFESET = frozenset(string.ascii_letters + string.digits + '@%_-+=:,./')

## Regex to match comma and quotes
_RE_COMMA_QUOTES = re.compile(r"\\.|[\"',]", re.DOTALL)

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
        if PY2:

            # Python 2.x only accepts this as input
            print(encoded)
        else:

            # Python 3.x and higher will allow remapping to
            # selected character encoding
            print(encoded.decode(sys.stdout.encoding))

########################################


try:
    # Test if basestring exists (Only in Python 2.x)
    basestring                                        # pylint: disable=W0104,basestring-builtin
    ## Internal type to pass to isinstance() for is_string()
    _IS_STRING_TEST = basestring                    # pylint: disable=C0103,basestring-builtin

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


def TrueFalse(item):            # pylint: disable=C0103
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


def TRUEFALSE(item):            # pylint: disable=C0103
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

########################################


def split_comma_with_quotes(comma_string):
    """
    Split comma seperated string while handling quotes

    str.split(',') will split a string into a list but it doesn't
    handle entries that are encased in quotes. This function will
    scan for quote characters and skip over any comma that's encased
    in quotes.

    Examples:
        # Result is ['"foo,bar"','foo','bar']
        lines = burger.strutils.split_comma_with_quotes('"foo,bar",foo,bar')

        # Will raise an error due to missing end quote
        willraise = burger.strutils.split_comma_with_quote('"foo,bar')

    Args:
        comma_string: String of comma seperated strings

    Return:
        List of string fragments for each comma seperated entries

    Raises:
        ValueError

    """

    # Start the parsing at the start of the string
    marker = 0

    # No delimiter found yet
    delimiter = ''
    result = []

    # Get list of matches
    for match in _RE_COMMA_QUOTES.finditer(comma_string):

        # Get the character that matched
        temp = match.group(0)

        # Looking for a comma?
        if delimiter == '':

            # This is a comma that will trigger a split
            if temp == ',':

                # Add in the string that was found
                result.append(comma_string[marker:match.start()])
                # Mark AFTER the comma with +1
                marker = match.start() + 1

            # Is this a quote?
            elif temp in "\"'":
                # Mark a delimiter and stop checking for commas
                delimiter = temp

        # A delimiter is being tracker, has it been hit?
        elif temp == delimiter:
            # Enable splitting on commas
            delimiter = ''

    # If the quote was not matched, throw an exception
    if delimiter:
        raise ValueError("String wasn't properly quoted")

    # Grab the last string chunk
    temp = comma_string[marker:]

    # If it's empty, it's because there was a trailing comma
    if temp:
        result.append(temp)

    return result

########################################


def parse_csv(csv_string):
    """
    Parse a comma seperated string allowing quoted strings

    Given a string of comma seperated entries and handle quotes properly.

    Examples:
        # Result is ['foo,bar','foo','bar']
        lines = burger.strutils.split_comma_with_quotes('"foo,bar",foo,bar')

        # Result is ['foo"bar',"'boo'boo'"]
        lines = burger.strutils.split_comma_with_quotes('"foo""bar","'boo,boo'")

        # Will raise an error due to missing end quote
        willraise = burger.strutils.split_comma_with_quote('"foo,bar')

    Args:
        csv_string: String of comma seperated entries
    Returns:
        List of entries with whitespace stripped from prefix and suffix
    Raises:
        ValueError
    """

    result = []
    # Seperate by commas
    for item in split_comma_with_quotes(csv_string):

        # Strip the whitespace
        temp = item.strip('\n\r \t')

        # Is there anything to parse?
        if temp:

            # Check if there's a delimiter
            delimiter = temp[0]
            if delimiter in "\"'":

                # If there's a delimiter, properly handle it
                temp = next(csv.reader([temp], quotechar=str(delimiter), \
                    delimiter=str(delimiter), quoting=csv.QUOTE_ALL))[0]
        result.append(temp)
    return result

########################################


def translate_to_regex_match(file_list):
    """
    Translate filename wildcards into regexes.

    Args:
        file_list: List of filename wildcards
    Results:
        List of re.compile().match entries
    """

    # Start with an empty folder
    result = []
    for item in convert_to_array(file_list):
        # Translate and then return the match function
        result.append(re.compile(fnmatch.translate(item)).match)
    return result

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
