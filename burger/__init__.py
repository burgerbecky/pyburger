#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of subroutines used by the Burgerlib based scripts written in Python.

@package burger

For higher level tools like makeprojects, cleanme and
buildme, common subroutines were collected and
placed in this module for reuse.

@mainpage

@htmlinclude README.html

Chapter list
============

- @subpage md_truefalse
- @subpage md_wsl__cygwin
- @subpage md_find__visual__studio
- @subpage md_validators

Module list
============

- @ref burger
- @ref burger.buildutils
- @ref burger.cleanutils
- @ref burger.fileutils
- @ref burger.locators
- @ref burger.strutils
- @ref burger.validators
- @ref burger.windowsutils

@var burger.__numversion__
Numeric version

@var burger.__version__
Current version of the library

@var burger.__author__
Author's name

@var burger.__title__
Name of the module

@var burger.__summary__
Summary of the module's use

@var burger.__uri__
Home page

@var burger.__email__
Email address for bug reports

@var burger.__license__
Type of license used for distribution

@var burger.__copyright__
Copyright owner

@var burger.__all__
Items to import on "from burger import *"

"""

# pylint: disable=redundant-u-string-prefix
# pylint: disable=import-error
# pylint: disable=super-with-arguments
# pyright: reportMissingImports=false

from __future__ import absolute_import

import sys

from .strutils import PY2, unicode_print, is_string, convert_to_array, \
    norm_paths, string_to_bool, \
    TrueFalse, truefalse, TRUEFALSE, convert_to_windows_slashes, \
    convert_to_linux_slashes, encapsulate_path_windows, \
    encapsulate_path_linux, encapsulate_path, encapsulate_hosted_path, \
    split_comma_with_quotes, parse_csv, translate_to_regex_match, \
    host_machine, get_windows_host_type, get_mac_host_type, \
    escape_xml_cdata, escape_xml_attribute, packed_paths, \
    make_version_tuple

from .fileutils import is_write_protected, make_executable, \
    create_folder_if_needed, delete_file, is_source_newer, \
    copy_file_if_needed, copy_directory_if_needed, shutil_readonly_cb, \
    delete_directory, clean_directories, clean_files, get_tool_path, \
    traverse_directory, unlock_files, lock_files, load_text_file, \
    save_text_file, compare_files, compare_file_to_string, \
    read_zero_terminated_string, save_text_file_if_newer, \
    environment_root

from .buildutils import get_sdks_folder, fix_csharp, is_exe, get_path_ext, \
    make_exe_path, find_in_path, expand_and_verify, run_command, \
    is_codewarrior_mac_allowed, import_py_script, run_py_script, \
    execfile

from .locators import where_is_codeblocks, where_is_watcom, \
    where_is_doxygen, where_is_pdflatex, where_is_makeindex, \
    where_is_visual_studio

from .perforce import where_is_p4, is_under_p4_control, perforce_command, \
    perforce_edit, perforce_add, perforce_opened, make_version_header

from .git import where_is_git, is_under_git_control, make_git_version_header

from .cleanutils import clean_xcode, clean_codeblocks, clean_setup_py

from .validators import BooleanProperty, StringProperty, IntegerProperty, \
    StringListProperty, EnumProperty, NoneProperty

from .windowsutils import find_visual_studios

from .xcode import where_is_xcode, find_rez_headers, build_rez

if PY2:
    from cStringIO import StringIO
else:
    from io import StringIO

########################################


# Numeric version
__numversion__ = (1, 4, 6)

# Current version of the library
__version__ = ".".join([str(num) for num in __numversion__])

# Author's name
__author__ = "Rebecca Ann Heineman"

# Name of the module
__title__ = "burger"

# Summary of the module's use
__summary__ = "Burger Becky's shared python library."

# Home page
__uri__ = "http://pyburger.readthedocs.io"

# Email address for bug reports
__email__ = "becky@burgerbecky.com"

# Type of license used for distribution
__license__ = "MIT License"

# Copyright owner
__copyright__ = "Copyright 2013-2025 Rebecca Ann Heineman"

# Items to import on "from burger import *"
__all__ = [
    "unicode_print",
    "is_string",
    "convert_to_array",
    "norm_paths",
    "string_to_bool",
    "TrueFalse",
    "truefalse",
    "TRUEFALSE",
    "convert_to_windows_slashes",
    "convert_to_linux_slashes",
    "encapsulate_path_windows",
    "encapsulate_path_linux",
    "encapsulate_path",
    "encapsulate_hosted_path",
    "split_comma_with_quotes",
    "parse_csv",
    "translate_to_regex_match",
    "host_machine",
    "get_windows_host_type",
    "get_mac_host_type",
    "escape_xml_cdata",
    "escape_xml_attribute",
    "packed_paths",
    "make_version_tuple",
    "is_write_protected",
    "make_executable",
    "create_folder_if_needed",
    "delete_file",
    "is_source_newer",
    "copy_file_if_needed",
    "copy_directory_if_needed",
    "shutil_readonly_cb",
    "delete_directory",
    "clean_directories",
    "clean_files",
    "get_tool_path",
    "traverse_directory",
    "unlock_files",
    "lock_files",
    "load_text_file",
    "save_text_file",
    "compare_files",
    "compare_file_to_string",
    "read_zero_terminated_string",
    "save_text_file_if_newer",
    "environment_root",
    "get_sdks_folder",
    "fix_csharp",
    "is_exe",
    "get_path_ext",
    "make_exe_path",
    "find_in_path",
    "expand_and_verify",
    "run_command",
    "is_codewarrior_mac_allowed",
    "import_py_script",
    "run_py_script",
    "execfile",
    "where_is_codeblocks",
    "where_is_watcom",
    "where_is_doxygen",
    "where_is_pdflatex",
    "where_is_makeindex",
    "where_is_visual_studio",
    "where_is_p4",
    "is_under_p4_control",
    "perforce_command",
    "perforce_edit",
    "perforce_add",
    "perforce_opened",
    "make_version_header",
    "where_is_git",
    "is_under_git_control",
    "make_git_version_header",
    "Interceptstdout",
    "Node",
    "clean_xcode",
    "clean_codeblocks",
    "clean_setup_py",
    "BooleanProperty",
    "IntegerProperty",
    "StringProperty",
    "StringListProperty",
    "EnumProperty",
    "NoneProperty",
    "find_visual_studios",
    "where_is_xcode",
    "find_rez_headers",
    "build_rez"
]

########################################


class Interceptstdout(list):
    """
    Handy class for capturing stdout from tools and python itself.

    Attributes:
        _stdout: Saved copy of sys.stdout
        _stringio: StringIO to redirect output to

    Examples:
        # Import the class
        from burger import Interceptstdout

        # Instanciate the class, which intercepts stdout
        with Interceptstdout() as output:
            do_somethingthatprints()
            print("capture me!")

        # Once out of scope, output has a list of strings
        # of the captured stdout output.
        print(output)

    """

    def __init__(self):
        """
        Declares the internal variables
        """

        super(Interceptstdout, self).__init__()
        self._stdout = None
        self._stringio = None

    def __enter__(self):
        """
        Invoked on "with" which intercepts all future stdout
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

    Attributes:
        value: Value contained in this node
        children: Array of children nodes to this node
    """

    def __init__(self, value, children=None):
        """
        Create a node with an initial value

        Args:
            value: Object to be the value of this node
            children: Array of nodes to be added as children to this one
        """

        if children is None:
            children = []

        self.value = value
        self.children = children

    def __repr__(self, level=0):
        """
        Display this node as a string

        Args:
            level: Recursion depth (Used internally)
        """

        ret = u"\t" * level + repr(self.value) + u"\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

    def __str__(self, level=0):
        """
        Display this node as a string

        Args:
            level: Recursion depth (Used internally)
        """

        return self.__repr__(level=0)
