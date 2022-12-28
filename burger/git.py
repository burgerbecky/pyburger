#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains git helper functions

Functions to locate git and issue git commands

@package burger.git

@var burger.git._GIT_PATH
Cached location of git
"""

from __future__ import absolute_import, print_function, unicode_literals

import os

try:
    from wslwinreg import convert_from_windows_path
except ImportError:
    pass

from .strutils import get_windows_host_type, IS_LINUX, get_mac_host_type

from .buildutils import is_exe, _WINDOWS_ENV_PATHS, find_in_path, \
    run_command, _create_header_guard

# Cached location of git
_GIT_PATH = None

########################################


def where_is_git(verbose=False, refresh=False, path=None):
    """
    Return the location of the git executable

    Look for an environment variable GIT and
    determine if the executable resides there, if
    so, return the string to the path.

    PATH is then searched for git, and if it's not found,
    None is returned.

    Args:
        verbose: If True, print a message if git was not found
        refresh: If True, reset the cache and force a reload.
        path: Path to git to place in the cache
    Returns:
        A path to the git command line executable or None if not found.
    See Also:
        where_is_p4, is_under_git_control
    """
    # pylint: disable=too-many-branches

    # pylint: disable=global-statement
    global _GIT_PATH

    # Clear the cache if needed
    if refresh:
        _GIT_PATH = None

    # Set the override, if found
    if path:
        _GIT_PATH = path

    # Is cached?
    if _GIT_PATH:
        return _GIT_PATH

    # Try the environment variable first
    if os.getenv("GIT", None):
        if get_windows_host_type(True):

            # Windows points to the base path
            gitpath = os.path.expandvars("${GIT}\\git.exe")
            gitpath = convert_from_windows_path(gitpath)
            if is_exe(gitpath):
                _GIT_PATH = gitpath
                return gitpath
            # Try a second time using the bin folder
            gitpath = os.path.expandvars("${GIT}\\bin\\git.exe")
            gitpath = convert_from_windows_path(gitpath)
        else:
            # Just append the exec name
            gitpath = os.path.expandvars("${GIT}/git")

        # Valid?
        if is_exe(gitpath):
            _GIT_PATH = gitpath
            return gitpath

    # Scan the PATH for the exec
    gitpath = find_in_path("git", executable=True)
    if gitpath:
        _GIT_PATH = gitpath
        return gitpath

    # List of the usual suspects
    full_paths = []

    # Check if it's installed but not in the path
    if get_windows_host_type(True):

        # Try the "ProgramFiles" folders
        for item in _WINDOWS_ENV_PATHS:
            if os.getenv(item, None):
                gitpath = os.path.expandvars(
                    "${" + item + "}\\git\\bin\\git.exe")
                gitpath = convert_from_windows_path(gitpath)
                full_paths.append(gitpath)

    elif get_mac_host_type():

        # Installed here via brew
        full_paths.append("/opt/local/bin/git")

    if IS_LINUX:
        # Posix / Linux
        full_paths.append("/usr/bin/git")

    # Scan the list of known locations
    for gitpath in full_paths:
        if is_exe(gitpath):
            # Finally found it!
            _GIT_PATH = gitpath
            return gitpath

    # Oh, dear.
    if verbose:
        print("git not found!")
        if get_mac_host_type():
            print("Use brew or macports for the command line version")

    # Can't find it
    return None

########################################


def is_under_git_control(working_directory):
    """
    Test if the directory is under git source control.

    First test if git is installed by calling where_is_git(). Then
    use the git tool to query if the working directory is under git
    source control.

    Args:
        working_directory: Directory to test.
    Returns:
        True if the directory is under git control, False if not.
    See Also:
        where_is_git
    """

    gitpath = where_is_git()
    if gitpath:
        if not run_command(
            (gitpath, "rev-parse"),
                working_directory, True, True, True)[0]:
            return True
    return False

########################################


def _call_git(cmd, working_dir, verbose):
    """
    Call git and return the output.

    If an error occured, return None for the string.

    Args:
        cmd: Tuple of the command line to execute
        working_dir: Directory to set before executing the command
        verbose: True for verbose output.
    Returns:
        Error code integer, returned string from git.
    """

    # Output the command line if requested
    if verbose:
        print(" ".join(cmd))

    # Perform the command
    # If verbose output is enabled, allow git to print the error
    error, tempdata = run_command(
        cmd, working_dir, capture_stdout=True, capture_stderr=not verbose)[:2]

    # If there was an error, discard the output.
    if error:
        return error, None

    # All good
    return error, tempdata.strip()

########################################


def make_git_version_header(working_dir, outputfilename, verbose=False):
    """
    Create a C header with the git version.

    This function assumes version control is with git!

    Get the last change list and tag, and then create a header
    with this information (Only modify the output file if
    the contents have changed)

    C++ defines are declared for GIT_HASH, GIT_CHANGEDATE, GIT_CHANGETIME,
    GIT_TAG_VERSION, and GIT_TAG_VERSION_INFO

    Args:
        working_dir: string with the path of the folder to obtain the git
            version for
        outputfilename: string with the path of the generated header
        verbose: Print git commands and other informational messages

    Returns:
        Zero if no error, non-zero on error
    """

    # pylint: disable=too-many-branches

    # Check if git is installed
    gitexe = where_is_git()
    if gitexe is None:
        return 10

    # Create the header guard by taking the filename,
    # converting to upper case and replacing spaces and
    # periods with underbars.
    headerguard = _create_header_guard(outputfilename)

    # Get the last hash
    error, git_hash = _call_git(
        (gitexe, "rev-parse", "HEAD"),
        working_dir, verbose)

    # The only way there is an error, is if this directory is not controlled
    # by git.
    if error:
        return error

    # Get the current branch
    error, git_branch = _call_git(
        (gitexe, "rev-parse", "--abbrev-ref", "HEAD"),
        working_dir, verbose)

    # Get the git tag
    error, git_tag = _call_git(
        (gitexe, "describe", "--tags", "--abbrev=0"),
        working_dir, verbose)

    # Get the full git tag
    error, git_full_tag = _call_git(
        (gitexe, "describe", "--tags", "--long"),
        working_dir, verbose)

    # Write out the header

    output = [
        "/***************************************",
        "",
        "\tThis file was generated by a call to",
        "\tburger.git.make_git_version_header() from",
        "\tthe burger python package",
        "",
        "***************************************/",
        "",
        "#ifndef " + headerguard,
        "#define " + headerguard,
        ""]

    if git_hash:
        output.append("#define GIT_HASH \"" + git_hash + "\"")

    if git_branch:
        output.append("#define GIT_BRANCH \"" + git_branch + "\"")

    if git_full_tag:
        output.append("#define GIT_FULL_TAG \"" + git_full_tag + "\"")

    if git_tag:
        output.append("#define GIT_TAG \"" + git_tag + "\"")

    output.extend(["", "#endif"])

    # Check if the data is different than what's already stored on
    # the drive
    # pylint: disable=import-outside-toplevel
    from .fileutils import compare_file_to_string, save_text_file
    if compare_file_to_string(outputfilename, output) is False:
        if verbose:
            print("Writing " + outputfilename)
        try:
            save_text_file(outputfilename, output)
        except IOError as error:
            print(error)
            return 2
    return 0
