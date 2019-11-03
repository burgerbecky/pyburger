#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of subroutines used by the Burgerlib based scripts written in Python.
"""

# pylint: disable=C0302

#
## \package burger
#
# For higher level tools like makeprojects, cleanme and
# buildme, common subroutines were collected and
# placed in this module for reuse.
#

#
## \mainpage
#
# \htmlinclude README.html
#
#
# Module list
# ===========
#
# - \ref burger
# - \ref burger.buildutils
# - \ref burger.cleanutils
# - \ref burger.fileutils
# - \ref burger.strutils
# - \ref burger.validators
# - \ref burger.windowsutils
#

from __future__ import absolute_import, print_function, unicode_literals

import sys

from .__pkginfo__ import NUMVERSION, VERSION, AUTHOR, TITLE, SUMMARY, URI, \
    EMAIL, LICENSE, COPYRIGHT

from .strutils import PY2, unicode_print, is_string, convert_to_array, \
    string_to_bool, \
    TrueFalse, truefalse, TRUEFALSE, convert_to_windows_slashes, \
    convert_to_linux_slashes, encapsulate_path_windows, \
    encapsulate_path_linux, encapsulate_path, split_comma_with_quotes, \
    parse_csv, translate_to_regex_match, host_machine, get_windows_host_type, \
    get_mac_host_type, escape_xml_cdata, escape_xml_attribute, \
    packed_paths, from_cygwin_path, to_cygwin_path, from_wsl_path, \
    to_wsl_path, from_windows_host_path, to_windows_host_path

from .fileutils import is_write_protected, make_executable, \
    create_folder_if_needed, delete_file, is_source_newer, \
    copy_file_if_needed, copy_directory_if_needed, shutil_readonly_cb, \
    delete_directory, clean_directories, clean_files, get_tool_path, \
    traverse_directory, unlock_files, lock_files, load_text_file, \
    save_text_file, compare_files, compare_file_to_string, \
    read_zero_terminated_string, save_text_file_if_newer

from .buildutils import get_sdks_folder, fix_csharp, is_exe, get_path_ext, \
    make_exe_path, find_in_path, where_is_doxygen, \
    where_is_p4, expand_and_verify, perforce_command, perforce_edit, \
    perforce_add, perforce_opened, where_is_watcom, run_command, \
    make_version_header, is_codewarrior_mac_allowed, import_py_script, \
    run_py_script, where_is_visual_studio, where_is_codeblocks, \
    where_is_xcode

from .cleanutils import clean_xcode, clean_codeblocks, clean_setup_py

from .validators import BooleanProperty, StringProperty, IntegerProperty, \
    StringListProperty, EnumProperty, NoneProperty

from .windowsutils import get_file_info

# pylint: disable=C0302

if PY2:
    from cStringIO import StringIO  # pylint: disable=F0401
else:
    from io import StringIO

########################################


## Numeric version
__numversion__ = NUMVERSION

## Current version of the library
__version__ = VERSION

## Author's name
__author__ = AUTHOR

## Name of the module
__title__ = TITLE

## Summary of the module's use
__summary__ = SUMMARY

## Home page
__uri__ = URI

## Email address for bug reports
__email__ = EMAIL

## Type of license used for distribution
__license__ = LICENSE

## Copyright owner
__copyright__ = COPYRIGHT

## Items to import on "from burger import *"
__all__ = [
    'unicode_print',
    'is_string',
    'convert_to_array',
    'string_to_bool',
    'TrueFalse',
    'truefalse',
    'TRUEFALSE',
    'convert_to_windows_slashes',
    'convert_to_linux_slashes',
    'encapsulate_path_windows',
    'encapsulate_path_linux',
    'encapsulate_path',
    'split_comma_with_quotes',
    'parse_csv',
    'translate_to_regex_match',
    'host_machine',
    'get_windows_host_type',
    'get_mac_host_type',
    'escape_xml_cdata',
    'escape_xml_attribute',
    'packed_paths',
    'from_cygwin_path',
    'to_cygwin_path',
    'from_wsl_path',
    'to_wsl_path',
    'from_windows_host_path',
    'to_windows_host_path',
    'is_write_protected',
    'make_executable',
    'create_folder_if_needed',
    'delete_file',
    'is_source_newer',
    'copy_file_if_needed',
    'copy_directory_if_needed',
    'shutil_readonly_cb',
    'delete_directory',
    'clean_directories',
    'clean_files',
    'get_tool_path',
    'traverse_directory',
    'unlock_files',
    'lock_files',
    'load_text_file',
    'save_text_file',
    'compare_files',
    'compare_file_to_string',
    'read_zero_terminated_string',
    'save_text_file_if_newer',
    'get_sdks_folder',
    'fix_csharp',
    'is_exe',
    'get_path_ext',
    'make_exe_path',
    'find_in_path',
    'where_is_doxygen',
    'expand_and_verify',
    'where_is_p4',
    'perforce_command',
    'perforce_edit',
    'perforce_add',
    'perforce_opened',
    'where_is_watcom',
    'run_command',
    'make_version_header',
    'is_codewarrior_mac_allowed',
    'import_py_script',
    'run_py_script',
    'where_is_visual_studio',
    'where_is_codeblocks',
    'where_is_xcode',
    'Interceptstdout',
    'Node',
    'clean_xcode',
    'clean_codeblocks',
    'clean_setup_py',
    'BooleanProperty',
    'IntegerProperty',
    'StringProperty',
    'StringListProperty',
    'EnumProperty',
    'NoneProperty',
    'get_file_info'
]

########################################


class Interceptstdout(list):
    """
    Handy class for capturing stdout from tools and python itself.

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
        Disconnect the stdout and store the items into a list of lines.
        @details
        Using splitlines(), output the buffer into a list of lines into the
        output field.
        """

        # Restore stdout on exit
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
        self._stringio = None
        self._stdout = None

########################################


class Node:
    """
    Node class for creating directory trees.

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

        ret = '\t' * level + repr(self.value) + '\n'
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    ## Display this node as a string
    # See Also:
    # __repr__()
    __str__ = __repr__
