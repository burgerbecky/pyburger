#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains executable locators

@package burger.locators

@var burger.buildutils._CODEBLOCKS_PATH
Cached location of CodeBlocks
"""

# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals

import os

try:
    from wslwinreg import convert_from_windows_path, OpenKey, CloseKey, \
        KEY_READ, HKEY_CURRENT_USER, KEY_WOW64_32KEY, QueryValueEx
except ImportError:
    pass

from .strutils import PY3_4_OR_HIGHER, get_mac_host_type, get_windows_host_type, \
    IS_LINUX

from .buildutils import is_exe, find_in_path, _WINDOWS_ENV_PATHS

# Cached location of CodeBlocks
_CODEBLOCKS_PATH = None

########################################


def where_is_xcode(xcode_version=None):
    """
    Locate xcodebuild for a specific version of XCode.

    Given a specific version by version, scan the locations that the IDE would
    be found.

    Example:
        >>> burger.where_is_xcode()
        ("/Developer/usr/bin/xcodebuild", 3)
        >>> burger.where_is_xcode(2093)
        None

    Note:
        This function will always return None on non-macOS hosts.
        Minimum version of XCode is 3.

    Args:
        xcode_version: Version number
    Returns:
        Path to xcodebuild for the XCode version or None.
    """

    # pylint: disable=too-many-branches

    # Test if running on a mac host
    host_type = get_mac_host_type()
    if not host_type:
        return None

    # Only import on macosx hosts
    # pylint: disable=import-outside-toplevel
    import plistlib

    # XCode 5 and higher reside in the app folder
    highest_version = 0
    xcodebuild = None

    # Version 3 and 4 is in /Developer while all
    # others are in /Applications

    dir_list = []
    if xcode_version is None or xcode_version < 5:
        dir_list.append("/Developer/Applications")
    if xcode_version is None or xcode_version > 3:
        dir_list.append("/Applications")

    for base_dir in dir_list:
        # Check if the directory exists first
        if os.path.isdir(base_dir):

            # Scan the applications folder for all apps called "XCode"
            for item in os.listdir(base_dir):

                # Scan only apps whose name starts with xcode
                if not item.lower().startswith("xcode"):
                    continue

                temp_path = base_dir + "/" + item + "/Contents/version.plist"
                try:
                    # pylint: disable=no-member
                    if PY3_4_OR_HIGHER:
                        with open(temp_path, "rb") as filefp:
                            version_dict = plistlib.load(filefp)
                    else:
                        version_dict = plistlib.readPlist(
                            temp_path)

                # Any IO error is acceptable to ignore
                except IOError:
                    continue

                version = version_dict.get("CFBundleShortVersionString", None)
                if not version:
                    continue

                # Check the version for a match
                version = int(version.split(".")[0])

                # XCode 3 is hard coded to Developer
                if version == 3:
                    temp_path = "/Developer/usr/bin/xcodebuild"
                else:
                    temp_path = (
                        "{}/{}/Contents/Developer"
                        "/usr/bin/xcodebuild").format(base_dir, item)

                if not os.path.isfile(temp_path):
                    continue

                if xcode_version:
                    # If scanning for a perfect match, exit if found
                    if version == xcode_version:
                        highest_version = version
                        return (temp_path, version)

                # Scan for the most recent version of XCode
                elif version > highest_version:
                    highest_version = version
                    xcodebuild = (temp_path, version)

    # XCode 3 is hard coded to a specific location
    if (not xcode_version and not highest_version) or xcode_version == 3:
        # On OSX Lion and higher, XCode 3.1.4 is a separate folder
        for item in ("/Xcode3.1.4/usr/bin/xcodebuild",):
            if os.path.isfile(item):
                xcodebuild = (item, 3)
                break

    return xcodebuild

########################################


def _get_codeblocks_registry_path():
    """
    Locate codeblocks path using the Window Registry

    Private function only called on Windows hosts to query the registry for the
    location of Codeblocks.

    Check HKCU\\SOFTWARE\\CodeBlocks\\Path for the base directory of CodeBlocks
    on Windows.

    Returns:
        None or a string with the path to CodeBlocks
    """

    # Open the registry key
    try:
        key = OpenKey(HKEY_CURRENT_USER, "SOFTWARE\\CodeBlocks",
                      0, KEY_READ | KEY_WOW64_32KEY)
    except FileNotFoundError:
        return None

    # If a key was found, get the path
    codeblocks_path, _ = QueryValueEx(key, "Path")
    CloseKey(key)

    # Convert to path
    codeblocks_path = codeblocks_path + "\\codeblocks.exe"

    # Convert to Linux/Windows/Cygwin
    return convert_from_windows_path(codeblocks_path)


########################################


def where_is_codeblocks(verbose=False, refresh=False, path=None):
    """
    Return the location of CodeBlocks's executable.

    Look for an environment variable CODEBLOCKS and determine if the executable
    resides there, if so, return the string to the path

    If running on a MacOSX client, look in the Applications folder for a copy of
    CodeBlocks.app and return the pathname to the copy of CodeBlocks that
    resides within

    PATH is then searched for CodeBlocks, and if it's not found, None is
    returned.

    Args:
        verbose: If True, print a message if CodeBlocks was not found
        refresh: If True, reset the cache and force a reload.
        path: Path to CodeBlocks to place in the cache

    Returns:
        A path to the CodeBlocks command line executable or None if not found.

    """

    # pylint: disable=too-many-branches

    # pylint: disable=global-statement
    global _CODEBLOCKS_PATH

    # Clear the cache if needed
    if refresh:
        _CODEBLOCKS_PATH = None

    # Set the override, if found
    if path:
        _CODEBLOCKS_PATH = path

    # Is cached?
    if _CODEBLOCKS_PATH:
        return _CODEBLOCKS_PATH

    # Try the environment variable first
    codeblocks_env = os.getenv("CODEBLOCKS", None)
    if codeblocks_env:
        if get_windows_host_type(True):

            # Windows points to the base path
            codeblocks_path = convert_from_windows_path(
                codeblocks_env + "\\codeblocks.exe")
        else:
            # Just append the exec name
            codeblocks_path = os.path.expandvars("${CODEBLOCKS}/CodeBlocks")

        # Valid?
        if is_exe(codeblocks_path):
            _CODEBLOCKS_PATH = codeblocks_path
            return codeblocks_path

    # Scan the PATH for the exec
    codeblocks_path = find_in_path("CodeBlocks", executable=True)
    if codeblocks_path:
        _CODEBLOCKS_PATH = codeblocks_path
        return codeblocks_path

    # List of the usual suspects
    full_paths = []

    # Check if it's installed but not in the path
    if get_windows_host_type(True):

        # Check the registry
        codeblocks_path = _get_codeblocks_registry_path()
        if codeblocks_path:
            full_paths.append(codeblocks_path)

        # Try the "ProgramFiles" folders
        # Note: May not be visible in WSL
        for item in _WINDOWS_ENV_PATHS:
            if os.getenv(item, None):
                codeblocks_path = os.path.expandvars(
                    "${" + item + "}\\CodeBlocks\\codeblocks.exe")
                codeblocks_path = convert_from_windows_path(codeblocks_path)
                full_paths.append(codeblocks_path)

    elif get_mac_host_type():

        # MacOSX has it hidden in the application
        full_paths.append(
            "/Applications/CodeBlocks.app/Contents/MacOS/CodeBlocks")
        full_paths.append("/opt/local/bin/CodeBlocks")

    if IS_LINUX:
        # Posix / Linux
        full_paths.append("/usr/bin/codeblocks")
        full_paths.append("/usr/bin/CodeBlocks")

    # Scan the list of known locations
    for codeblocks_path in full_paths:
        if is_exe(codeblocks_path):
            # Finally found it!
            _CODEBLOCKS_PATH = codeblocks_path
            return codeblocks_path

    # Oh, dear.
    if verbose:
        print("CodeBlocks not found!")
        if get_mac_host_type():
            print("Install the desktop application in the Applications folder")

    # Can't find it
    return None
