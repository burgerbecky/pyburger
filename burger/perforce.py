#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains functions to help perforce

@package burger.perforce

@var burger.perforce._PERFORCE_PATH
Cached location of p4 from Perforce
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import subprocess

try:
    from wslwinreg import convert_from_windows_path, convert_to_windows_path
except ImportError:
    pass

from .strutils import is_string, IS_LINUX, get_windows_host_type, \
    get_mac_host_type

from .buildutils import is_exe, find_in_path, _create_header_guard, \
    run_command, _WINDOWS_ENV_PATHS

# Cached location of p4 from Perforce
_PERFORCE_PATH = None

########################################


def where_is_p4(verbose=False, refresh=False, path=None):
    """
    Return the location of the p4 executable

    Look for an environment variable PERFORCE and
    determine if the executable resides there, if
    so, return the string to the path.

    PATH is then searched for p4, and if it's not found,
    None is returned.

    Args:
        verbose: If True, print a message if Perforce was not found
        refresh: If True, reset the cache and force a reload.
        path: Path to Perforce to place in the cache
    Returns:
        A path to the Perforce command line executable or None if not found.
    See Also:
        perforce_edit, perforce_add, where_is_git, is_under_p4_control
    """

    # pylint: disable=too-many-branches

    # pylint: disable=global-statement
    global _PERFORCE_PATH

    # Clear the cache if needed
    if refresh:
        _PERFORCE_PATH = None

    # Set the override, if found
    if path:
        _PERFORCE_PATH = path

    # Is cached?
    if _PERFORCE_PATH:
        return _PERFORCE_PATH

    # Try the environment variable first
    if os.getenv("PERFORCE", None):
        if get_windows_host_type(True):

            # Windows points to the base path
            p4path = os.path.expandvars("${PERFORCE}\\p4.exe")
            p4path = convert_from_windows_path(p4path)
        else:
            # Just append the exec name
            p4path = os.path.expandvars("${PERFORCE}/p4")

        # Valid?
        if is_exe(p4path):
            _PERFORCE_PATH = p4path
            return p4path

    # Scan the PATH for the exec
    p4path = find_in_path("p4", executable=True)
    if p4path:
        _PERFORCE_PATH = p4path
        return p4path

    # List of the usual suspects
    full_paths = []

    # Check if it's installed but not in the path
    if get_windows_host_type(True):

        # Try the "ProgramFiles" folders
        for item in _WINDOWS_ENV_PATHS:
            if os.getenv(item, None):
                p4path = os.path.expandvars(
                    "${" + item + "}\\perforce\\p4.exe")
                p4path = convert_from_windows_path(p4path)
                full_paths.append(p4path)

    elif get_mac_host_type():

        # Installed here via brew
        full_paths.append("/opt/local/bin/p4")

    if IS_LINUX:
        # Posix / Linux
        full_paths.append("/usr/bin/p4")

    # Scan the list of known locations
    for p4path in full_paths:
        if is_exe(p4path):
            # Finally found it!
            _PERFORCE_PATH = p4path
            return p4path

    # Oh, dear.
    if verbose:
        print("Perforce \"p4\" not found!")
        if get_mac_host_type():
            print("Use brew or macports for the command line version")

    # Can't find it
    return None

########################################


def is_under_p4_control(working_directory):
    """
    Test if the directory is under Perforce source control.

    First test if p4 is installed by calling where_is_p4(). Then
    use the p4 tool to query if the working directory is under Perforce
    source control.

    Note:
        On folders that are not under Perforce control, p4 may take as
        much as 15 seconds to return a result, so use this call with caution.
    Args:
        working_directory: Directory to test.
    Returns:
        True if the directory is under Perforce control, False if not.
    See Also:
        where_is_p4
    """

    p4path = where_is_p4()
    if p4path:
        results = run_command(
            (p4path, "-s", "where", "..."),
            working_directory, True, True, True)
        p4output = results[1].splitlines()
        for item in p4output:
            if item.startswith("exit: "):
                i = int(item[6:])
                if not i:
                    return True
    return False

########################################


def perforce_command(files, command, verbose=False):
    """
    Given a list of files, send a command to execute on them in perforce

    Pass either a single string or a string list of pathnames
    of files to checkout in perforce using the "p4" command with
    the command name

    Args:
        files: list or string object of file(s) to checkout
        command: string to pass to p4 such as "edit" or "add"
        verbose: If True, print the command line and warnings

    Returns:
        Zero if no error, non-zero on error
    See Also:
        where_is_p4
    """

    # Get the p4 executable
    perforce_path = where_is_p4(verbose=verbose)

    # Not found?
    if perforce_path is None:
        return 10

    # Encapsulate the single string entry
    if is_string(files):
        file_list = (files,)
    else:
        file_list = files

    # Generate the command line and call
    error = 0
    for item in file_list:
        item = os.path.abspath(item)
        # If p4.exe, it's windows. Use a windows pathname
        if not perforce_path.endswith("p4"):
            item = convert_to_windows_path(item)

        cmd = [perforce_path, command, item]
        if verbose:
            print(" ".join(cmd))
        error = subprocess.call(cmd)
        if error:
            break
    return error

########################################


def perforce_edit(files, verbose=False):
    """
    Given a list of files, checkout (Edit) them in perforce

    Pass either a single string or a string list of pathnames
    of files to checkout in perforce using the "p4 edit" command

    Args:
        files: list or string object of file(s) to checkout
        verbose: If True, print the command line and warnings

    Returns:
        Zero if no error, non-zero on error
    See Also:
        where_is_p4
    """

    # Perform the edit command
    return perforce_command(files, "edit", verbose=verbose)

########################################


def perforce_add(files, verbose=False):
    """
    Given a list of files, add them in perforce

    Pass either a single string or a string list of pathnames
    of files to checkout in perforce using the "p4 add" command

    Args:
        files: list or string object of file(s) to add
        verbose: If True, print the command line and warnings

    Returns:
        Zero if no error, non-zero on error
    See Also:
        where_is_p4
    """

    # Perform the edit command
    return perforce_command(files, "add", verbose=verbose)

########################################


def perforce_opened(files=None, verbose=False):
    """
    Get the list of opened files in Perforce.

    Check perforce if any files are opened and if so,
    return the list of files in Perforce format that
    are currently opened.

    Args:
        files: List of files or directories to check, None for all.
        verbose: If True, print the command line and warnings.

    Returns:
        List of opened files, can be empty if no files are opened.
    See Also:
        where_is_p4
    """

    # Get the p4 executable
    perforce_path = where_is_p4(verbose=verbose)

    # Not found?
    if perforce_path is None:
        return []

    cmd = [perforce_path, "opened"]

    # Add list of file(s) or directories to check
    if files:
        if is_string(files):
            cmd.append(files)
        else:
            cmd.extend(files)

    # Issue the command
    result = run_command(
        cmd,
        capture_stdout=True,
        capture_stderr=True,
        quiet=not verbose)

    # Was there an error?
    if result[2] != "":
        # Print the error on verbose output
        if verbose:
            print(result[2])
        return []
    # Perforce uses "#" as a delimiter from the filename
    # to the file version.
    return [x.split("#")[0] for x in result[1].splitlines()]

########################################


def make_version_header(working_dir, outputfilename, verbose=False):
    """
    Create a C header with the perforce version.

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
        verbose: Print perforce commands and other informational messages

    Returns:
        Zero if no error, non-zero on error
    """

    # pylint: disable=too-many-branches
    # Check if perforce is installed
    p4exe = where_is_p4()
    if p4exe is None:
        return 10

    # Create the header guard by taking the filename,
    # converting to upper case and replacing spaces and
    # periods with underbars.
    headerguard = _create_header_guard(outputfilename)

    # Get the last change list
    # Parse "Change 3361 on 2012/05/15 13:20:12 by burgerbecky@burgeroctocore
    # 'Made a p4 change'"
    # -m 1 / Limit to one entry
    # -t / Display the time
    # -l / Print out the entire changelist description

    cmd = (p4exe, "changes", "-m", "1", "-t", "-l", "...#have")
    if verbose:
        print(" ".join(cmd))
    error, tempdata = run_command(cmd, working_dir, capture_stdout=True)[:2]
    if error != 0:
        return error

    # Parse out the output of the p4 changes command
    p4changes = tempdata.strip().split(" ")

    # Get the p4 client
    # Parse "P4CLIENT=burgeroctocore (config)"

    cmd = (p4exe, "set", "P4CLIENT")
    if verbose:
        print(" ".join(cmd))
    error, tempdata = run_command(cmd, working_dir, capture_stdout=True)[:2]
    if error != 0:
        return error

    # Parse out the P4CLIENT query
    p4clients = tempdata.strip().split(" ", 1)[0].split("=")

    # Get the p4 user
    # Parse "P4USER=burgerbecky (config)"

    cmd = (p4exe, "set", "P4USER")
    if verbose:
        print(" ".join(cmd))
    error, tempdata = run_command(cmd, working_dir, capture_stdout=True)[:2]
    if error != 0:
        return error

    # Parse out the P4USER query
    p4users = tempdata.strip().split(" ", 1)[0].split("=")

    # Write out the header

    output = [
        "/***************************************",
        "",
        "\tThis file was generated by a call to",
        "\tburger.perforce.make_version_header() from",
        "\tthe burger python package",
        "",
        "***************************************/",
        "",
        "#ifndef " + headerguard,
        "#define " + headerguard,
        ""]

    if len(p4changes) > 4:
        output.append("#define P4_CHANGELIST " + p4changes[1])
        output.append("#define P4_CHANGEDATE \"" + p4changes[3] + "\"")
        output.append("#define P4_CHANGETIME \"" + p4changes[4] + "\"")

    if len(p4clients) > 1:
        output.append("#define P4_CLIENT \"" + p4clients[1] + "\"")

    if len(p4users) > 1:
        output.append("#define P4_USER \"" + p4users[1] + "\"")

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
