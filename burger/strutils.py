#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains string manipulation functions

@package burger.strutils

@var burger.strutils.PY2
True if the interpreter is Python 2.x

@var burger.strutils.PY3_OR_HIGHER
True if the interpreter is Python 3.x or higher

@var burger.strutils.PY3_3_OR_HIGHER
True if the interpreter is Python 3.3 or higher

@var burger.strutils.PY3_4_OR_HIGHER
True if the interpreter is Python 3.4 or higher

@var burger.strutils.PY3_5_OR_HIGHER
True if the interpreter is Python 3.5 or higher

@var burger.strutils.PYPY
True if the interpreter is PyPy

@var burger.strutils._WINDOWSSAFESET
Valid characters for windows filenames without quoting

@var burger.strutils._LINUXSAFESET
Valid characters for macOS and Linux files without quoting

@var burger.strutils._RE_COMMA_QUOTES
Regex to match comma and quotes

@var burger.strutils._MAC_HOST_TYPE
Cached result for get_mac_host_type()

@var burger.strutils.IS_LINUX
Running on linux?

@var burger.strutils.IS_MACOSX
Running on macOS X

@var burger.strutils.IS_WINDOWS
Running on Windows

@var burger.strutils.IS_CYGWIN
Running on Cygwin

@var burger.strutils.IS_MSYS
Running on MSYS

@var burger.strutils.IS_WSL
Running on Windows Subsystem for Linux

@var burger.strutils.IS_WINDOWS_HOST
Running on Windows (Including Linux shells on windows)

@var burger.strutils._WINDOWS_HOST_PREFIX
Prefix string for conversion of Windows paths to Linux.

@var burger.strutils._IS_STRING_TEST
Internal type to pass to isinstance() for is_string()

@var burger.strutils.UNICODE
Class for declaring unicode strings

@var burger.strutils.LONG
Class for declaring 64 bit integers
"""

# pylint: disable=consider-using-f-string
# pylint: disable=bad-option-value
# pyright: reportUndefinedVariable=false

from __future__ import absolute_import, print_function, unicode_literals

import sys
import os
import string
import re
import csv
import fnmatch
import platform
from numbers import Number

try:
    from wslwinreg import convert_to_windows_path
except ImportError:
    pass

# True if the interpreter is Python 2.x
PY2 = sys.version_info[0] == 2

# True if the interpreter is Python 3.x or higher
PY3_OR_HIGHER = sys.version_info[0] >= 3

# True if the interpreter is Python 3.3 or higher
PY3_3_OR_HIGHER = sys.version_info >= (3, 3, 0)

# True if the interpreter is Python 3.4 or higher
PY3_4_OR_HIGHER = sys.version_info >= (3, 4, 0)

# True if the interpreter is Python 3.5 or higher
PY3_5_OR_HIGHER = sys.version_info >= (3, 5, 0)

# True if the interpreter is PyPy
PYPY = platform.python_implementation() == 'PyPy'

# Valid characters for windows filenames without quoting
_WINDOWSSAFESET = frozenset(string.ascii_letters + string.digits + '_-.:\\')

# Valid characters for macOS and Linux files without quoting
_LINUXSAFESET = frozenset(string.ascii_letters + string.digits + '@%_-+=:,./')

# Regex to match comma and quotes
_RE_COMMA_QUOTES = re.compile(r"\\.|[\"',]", re.DOTALL)

# Cached result for get_mac_host_type()
_MAC_HOST_TYPE = None

# Running on linux?
IS_LINUX = sys.platform.startswith('linux')

# Running on macOS X
IS_MACOSX = sys.platform.startswith('darwin')

# Running on Windows
IS_WINDOWS = sys.platform.startswith('win')

# Running on Cygwin
IS_CYGWIN = sys.platform.startswith('cygwin')

# Running on MSYS
IS_MSYS = sys.platform.startswith('msys')

# Running on Windows Subsystem for Linux
IS_WSL = IS_LINUX and 'icrosoft' in platform.platform()

# Running on Windows (Including Linux shells on windows)
IS_WINDOWS_HOST = IS_WINDOWS or IS_CYGWIN or IS_MSYS or IS_WSL

if IS_CYGWIN:
    # Prefix string for conversion of Windows paths to Linux.
    _WINDOWS_HOST_PREFIX = '/cygdrive/'
elif IS_MSYS:
    _WINDOWS_HOST_PREFIX = '/'
elif IS_WSL:
    _WINDOWS_HOST_PREFIX = '/mnt/'
else:
    _WINDOWS_HOST_PREFIX = None

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
    # pylint: disable=pointless-statement
    basestring

    # Internal type to pass to isinstance() for is_string()
    _IS_STRING_TEST = basestring

    # Class for declaring unicode strings
    UNICODE = unicode

    # Class for declaring 64 bit integers
    LONG = long

except NameError:
    # Python 3 or later
    _IS_STRING_TEST = (str, bytes)
    UNICODE = str
    LONG = int


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


def norm_paths(working_directory, items):
    """
    Convert an iterable list of pathnames and convert them all into a
    list of normalized absolute pathnames.

    Args:
        working_directory: Base directory for incomplete paths
        items: Iterable list of pathnames
    Returns:
        A list of absolute pathnames
    """

    result = []
    for item in items:
        result.append(os.path.normpath(os.path.join(working_directory, item)))
    return result


########################################


def string_to_bool(item):
    """Convert an item to a boolean.

    Strings 'true', 't', ' on', 'yes', and, 'y' return True
    'false', 'f', 'off', 'no', and 'n' return False

    Non zero numbers or strings that are numbers become True
    Zero and '0' become False.

    Args:
        item: String or integer to convert.

    Returns:
        ``True`` or ``False``

    Exception:
        ValueError on invalid input.
    """

    # pylint: disable=too-many-return-statements
    # None becomes False
    if item is None:
        return False

    # Already a bool?
    if isinstance(item, bool):
        return item

    # Number to bool
    if isinstance(item, Number):
        return bool(item)

    if is_string(item):
        item_lower = item.lower()
        if item_lower in ('true', 't', 'on', 'yes', 'y'):
            return True
        if item_lower in ('false', 'f', 'off', 'no', 'n'):
            return False
        try:
            return bool(int(item))
        except ValueError:
            pass
        try:
            return bool(float(item))
        except ValueError:
            pass
    raise ValueError("Can't convert {} to bool".format(item))

########################################


def TrueFalse(item):            # pylint: disable=C0103
    """
    Convert the input into a boolean and return the string 'True' or 'False'

    If the input was a string of '0' or 'False' (Case insensitive comparision),
    this function will return 'False'. Empty dictionary, string or list
    objects, or the number zero will also return 'False'

    Args:
        item: Object to convert to a bool before converting into a string
    Returns:
        The string 'True' or 'False'
    See Also:
        truefalse, TRUEFALSE
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
    this function will return 'false'. Empty dictionary, string or list
    objects, or the number zero will also return 'false'

    Args:
        item: Object to convert to a bool before converting into a string
    Returns:
        The string 'true' or 'false'
    See Also:
        TRUEFALSE, TrueFalse
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
    this function will return 'FALSE'. Empty dictionary, string or list
    objects, or the number zero will also return 'FALSE'

    Args:
        item: Object to convert to a bool before converting into a string
    Returns:
        The string 'TRUE' or 'FALSE'
    See Also:
        truefalse, TrueFalse
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

    See Also:
        convert_to_linux_slashes

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

    See Also:
        convert_to_windows_slashes
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
    See Also:
        encapsulate_path
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
    See Also:
        encapsulate_path
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
    See Also:
        encapsulate_path_windows, encapsulate_path_linux
    """

    # Process for Windows platforms
    if IS_WINDOWS:
        return encapsulate_path_windows(input_path)

    # Force to linux slashes
    return encapsulate_path_linux(input_path)

########################################


def encapsulate_hosted_path(input_path):
    """
    Quote a pathname for use in the windows system shell

    If the platform is hosted on Windows, convert the pathname
    to Windows and then use Windows encapsulation rules.

    Args:
        input_path: string with the path to encapsulate
    Returns:
        Input string or input properly quoted
    See Also:
        encapsulate_path_windows, encapsulate_path_linux, encapsulate_path
    """

    # Process for Windows platforms
    if IS_WINDOWS_HOST:
        return encapsulate_path_windows(convert_to_windows_path(input_path))

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
        lines = burger.strutils.split_comma_with_quotes(
            '"foo""bar","'boo,boo'")

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
                temp = next(
                    csv.reader(
                        [temp],
                        quotechar=str(delimiter),
                        delimiter=str(delimiter),
                        quoting=csv.QUOTE_ALL))[0]
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

    See Also:
        get_mac_host_type, get_windows_host_type
    """

    # Is it ONLY windows, not hosted on windows?
    if IS_WINDOWS:
        return 'windows'

    # Is it macOS X?
    if IS_MACOSX:
        return 'macosx'

    if IS_LINUX or IS_CYGWIN or IS_MSYS or IS_WSL:
        # Assume linux or linux clones
        return 'linux'

    # Surrender Dorothy
    return 'unknown'

########################################


def get_windows_host_type(wsl_allowed=False):
    """
    Return windows host type (32 or 64 bit)

    Return False if the host is not Windows, 'x86' if it's a 32 bit host
    and 'x64' if it's a 64 bit host, and possibly 'arm' if an arm host

    Args:
        wsl_allowed: If True, allow returning a host type if cygwin
            is the shell.
    Returns:
        The string 'x64', 'x86', 'arm', 'arm64', 'ia64' or False
    See Also:
        get_mac_host_type, host_machine

    """

    # Not windows?
    if not IS_WINDOWS_HOST:
        return False

    # Is Linux under windows allowed?
    if not IS_WINDOWS:
        # Handle the case if host is Cygwin/msys/Linux running on windows
        if not wsl_allowed:
            return False

    # Test the CPU for the type

    machine = platform.machine().lower()
    if machine in ('amd64', 'x86_64', 'em64t'):
        return 'x64'
    if machine in ('arm64', 'arm', 'ia64'):
        return machine
    return 'x86'

########################################


def get_mac_host_type():
    """
    Return Mac OSX host type (PowerPC/Intel)

    Return False if the host is not Mac OSX. 'ppc' or 'ppc64' if it's a Power
    PC based system, 'x86' or 'x64' for Intel (Both 32 and 64 bit)

    Returns:
        The string 'x86', 'x64', 'ppc', 'ppc64' or False.

    See Also:
        get_windows_host_type, host_machine
    """

    global _MAC_HOST_TYPE       # pylint: disable=W0603
    if _MAC_HOST_TYPE is None:

        # Not macOS? Force returning False
        if not IS_MACOSX:
            cpu = False
        else:
            # Since it's a mac, query the Mac OSX cpu type
            # using the MacOSX python extensions

            cpu = platform.machine()

            # Intel 64 bit
            if cpu == 'x86_64':
                cpu = 'x64'

            # Special case for Power Macs
            elif cpu in ('PowerPC', 'ppc', 'Power Macintosh'):

                # Issue the command `machine` and capture the output.
                # If it contains 'ppc970' then you're running on a 64 bit
                # version of macOS, despite what platform.machine() says

                # pylint: disable=import-outside-toplevel
                from .buildutils import run_command
                if 'ppc970' in run_command('machine', capture_stdout=True)[1]:
                    cpu = 'ppc64'
                else:
                    cpu = 'ppc'
        _MAC_HOST_TYPE = cpu
    # Return the resolved global
    return _MAC_HOST_TYPE


########################################

def escape_xml_cdata(xml_string):
    """
    Convert escape codes for CDATA XML records.

    According to the XML docs, &, < and > cannot exist in a string
    so they must be replaced with "&amp;", "&lt;" and "&gt;" respectively.

    Args:
        xml_string: String to convert to one compatible with XML CDATA
    Return:
        Original string if no changes, or a new string with escaped characters.
    """

    # For speed, only perform the replace operation on strings that
    # actually need conversion.

    # IMPORTANT! Convert & first, since it will be inserted in
    # operations that follow.
    if '&' in xml_string:
        xml_string = xml_string.replace('&', '&amp;')

    if '<' in xml_string:
        xml_string = xml_string.replace('<', '&lt;')
    if '>' in xml_string:
        xml_string = xml_string.replace('>', '&gt;')
    return xml_string

########################################


def escape_xml_attribute(xml_string):
    """
    Convert escape codes for XML element attribute records.

    According to the XML docs, ", &, < and > cannot exist in a string
    so they must be replaced with "&quot'", &amp;", "&lt;" and "&gt;"
    respectively.

    Tabs and line feeds will be converted to "&#10;" and "&#09;".

    Note:
        https://www.w3.org/TR/REC-xml/#sec-line-ends
    Args:
        xml_string: String to convert to XML attribute strings.
    Return:
        Original string if no changes, or a new string with escaped characters.
    """

    # For speed, only perform the replace operation on strings that
    # actually need conversion.

    # Process &, < and >
    xml_string = escape_xml_cdata(xml_string)

    # Attributes are encased in quotes, escape the quote
    if '"' in xml_string:
        xml_string = xml_string.replace('"', '&quot;')

    # Line feeds need to be handled carefully because no one
    # can agree on \r, \n, \r\n, see note URL above
    if '\r\n' in xml_string:
        xml_string = xml_string.replace('\r\n', '&#10;')
    if '\r' in xml_string:
        xml_string = xml_string.replace('\r', '&#10;')
    if '\n' in xml_string:
        xml_string = xml_string.replace('\n', '&#10;')

    # Let's convert tabs
    if '\t' in xml_string:
        xml_string = xml_string.replace('\t', '&#09;')
    return xml_string

########################################


def packed_paths(entries, slashes=None, seperator=None,
                 force_ending_slash=False):
    """
    Convert a list of paths and convert to a PATH string.

    Convert ['a','b','c'] to a;b;c

    Args:
        entries: list of strings to concatenate
        slashes: None for no conversion, '/' or '\\' path seperator
        seperator: Character to use to seperate entries, ';' is used for None
        force_ending_slash: Enforce a trailing slash if True
    Return:
        String of all entries seperated by ';' or ``seperator``
    """

    # Verify the seperator
    if not seperator:
        seperator = ';'

    entries = convert_to_array(entries)

    # Slash functionality?
    if slashes:
        # Windows?
        if slashes == '\\':
            function = convert_to_windows_slashes
        else:
            # Everyone else use linux slashes
            function = convert_to_linux_slashes

        # Don't modify the original list
        temp_entries = []
        for item in entries:
            temp_entries.append(
                function(
                    item,
                    force_ending_slash=force_ending_slash))
    else:
        temp_entries = entries
    return seperator.join(temp_entries)

########################################


def make_version_tuple(version_string):
    """
    Convert numeric version string into an int tuple.

    Given a string like '1.0.5rc' and return a tuple of (1, 0, 5).
    The numbers are seperated by periods and members that start with
    a non number are skipped.

    Args:
        version_string: String for the version number.
    Returns:
        tuple of integers with the version. Can be an empty tuple.
    """

    if not version_string or not is_string(version_string):
        return tuple()

    result = []
    for item in version_string.split('.'):
        # If a pure number, convert to an int
        try:
            result.append(int(item))
        except ValueError:
            # None numeric, parse out the numbers
            found = re.findall(r'\d+', item)
            if not found:
                # Not a number? Abort here.
                break
            result.append(int(found[0]))
    return tuple(result)
