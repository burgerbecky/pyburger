#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Rules to build burger
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from burger import import_py_script, run_command

########################################


def do_clean(working_directory):
    """
    Delete all of the temporary files.

    Args:
        working_directory: Current directory
    """

    # The function exists in setup.py.
    # It can be manually invoked with "setup.py clean"
    setup = import_py_script(os.path.join(working_directory, 'setup.py'))
    setup.clean(working_directory)
    return 0

########################################


def do_build(working_directory):
    """
    Build the module so it's ready for upload to Pypi with Twine.

    Args:
        working_directory: Current directory
    """

    # Call setup.py to create the distribution files.
    run_command(
        ("python", "setup.py", "sdist", "bdist_wheel"),
        working_dir=working_directory)
    return 0

########################################


# pylint: disable=unused-argument
def rules(command, working_directory, root=True):
    """
    Main entry point for build_rules.py.

    When makeprojects, cleanme, or buildme is executed, they will call this
    function to perform the actions required for build customization.

    The parameter working_directory is required, and if it has no default
    parameter, this function will only be called with the folder that this
    file resides in. If there is a default parameter of None, it will be called
    with any folder that it is invoked on. If the default parameter is a
    directory, this function will only be called if that directory is desired.

    The optional parameter of root alerts the tool if subsequent processing of
    other build_rules.py files are needed or if set to have a default parameter
    of True, processing will end once the calls to this rules() function are
    completed.

    Commands are 'build', 'clean', 'prebuild', 'postbuild', 'project',
    'configurations'

    Arg:
        command: Command to execute.
        working_directory: Directory for this function to clean
        root: If set to True, exit cleaning upon completion of this function
    Return:
        Zero on success, non-zero on failure, and a list for 'configurations'

    """

    if command == 'clean':
        return do_clean(working_directory)
    if command == 'build':
        return do_build(working_directory)
    return 0


# If called as a command line and not a class, perform the build
if __name__ == "__main__":
    sys.exit(rules('build', os.path.dirname(os.path.abspath(__file__))))
