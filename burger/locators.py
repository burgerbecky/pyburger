#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains executable locators

Functions that will scan for executables so it's not necessary
for applications to either be on the PATH. They favor environement
variables, and then system registry before searching the path
and then looking at the usual hard coded locations

@package burger.locators

@var burger.locators._CODEBLOCKS_PATH
Cached location of CodeBlocks

@var burger.locators._WATCOM_PATH
Cached location of Watcom

@var burger.locators._DOXYGEN_PATH
Cached location of doxygen

@var burger.locators._VS_VARIANTS
Visual Studio variants in the order of search

@var burger.locators._VS_TABLE
Internal table of Visual Studio environment variables
"""

# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals

import os

try:
    from wslwinreg import convert_from_windows_path, OpenKey, CloseKey, \
        KEY_READ, HKEY_CURRENT_USER, KEY_WOW64_32KEY, QueryValueEx, \
        HKEY_LOCAL_MACHINE
except ImportError:
    pass

from .strutils import get_mac_host_type, get_windows_host_type, \
    IS_LINUX, convert_to_windows_slashes

from .buildutils import is_exe, find_in_path, _WINDOWS_ENV_PATHS

from .windowsutils import find_visual_studios

# Cached location of CodeBlocks
_CODEBLOCKS_PATH = None

# Cached location of Watcom
_WATCOM_PATH = None

# Cached location of doxygen
_DOXYGEN_PATH = None

# Visual Studio variants in the order of search
_VS_VARIANTS = (
    "Enterprise",
    "Professional",
    "Community"
)

# For each version of Visual Studio, set the default environment variable
# and path that the specific version of Visual Studio resides
_VS_TABLE = {
    2003: ("VS71COMNTOOLS", "Microsoft Visual Studio .NET 2003", 7),
    2005: ("VS80COMNTOOLS", "Microsoft Visual Studio 8", 8),
    2008: ("VS90COMNTOOLS", "Microsoft Visual Studio 9.0", 9),
    2010: ("VS100COMNTOOLS", "Microsoft Visual Studio 10.0", 10),
    2012: ("VS110COMNTOOLS", "Microsoft Visual Studio 11.0", 11),
    2013: ("VS120COMNTOOLS", "Microsoft Visual Studio 12.0", 12),
    2015: ("VS140COMNTOOLS", "Microsoft Visual Studio 14.0", 14),
    2017: ("VS150COMNTOOLS", "Microsoft Visual Studio\\2017\\xxx", 15),
    2019: ("VS160COMNTOOLS", "Microsoft Visual Studio\\2019\\xxx", 16),
    2022: ("VS170COMNTOOLS", "Microsoft Visual Studio\\2022\\xxx", 17)
}

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

########################################


def where_is_watcom(command=None, verbose=False, refresh=False, path=None):
    """
    Return the location of Watcom's executables.

    Look for an environment variable WATCOM and determine if the executable
    resides there, if so, return the string to the path

    In Windows, the boot drive is checked for a WATCOM folder and if found,
    that folder name is returned. If all checks failed, None is returned.

    Args:
        command: Watcom program to find.
        verbose: If True, print a message if watcom was not found
        refresh: If True, reset the cache and force a reload.
        path: Path to watcom to place in the cache

    Returns:
        A path to the Watcom folder or None if not found.
    """

    # pylint: disable=too-many-branches

    # pylint: disable=global-statement
    global _WATCOM_PATH

    # Clear the cache if needed
    if refresh:
        _WATCOM_PATH = None

    # Set the override, if found
    if path:
        _WATCOM_PATH = path

    # Windows .exe
    if get_windows_host_type(True):
        exe_folder = "binnt"
        suffix = ".exe"

    # Watcom is not available on macOS yet
    elif get_mac_host_type():
        return None

    # Linux
    else:
        exe_folder = "binl"
        suffix = ""

    # Append the system specific suffix
    if command:
        fake_command = command + suffix
    else:
        fake_command = "wcc386" + suffix

    # Is cached?
    if _WATCOM_PATH:
        if command:
            return os.path.join(_WATCOM_PATH, exe_folder, fake_command)
        return _WATCOM_PATH

    # Try the environment variable first
    watcom_path = os.getenv("WATCOM", None)
    if watcom_path:
        # Valid?
        if get_windows_host_type(True):
            watcom_path = convert_from_windows_path(watcom_path)
        full_path = os.path.join(watcom_path, exe_folder, fake_command)
        if is_exe(full_path):
            _WATCOM_PATH = watcom_path
            return full_path if command else watcom_path

    # List of the usual suspects
    full_paths = []
    if get_windows_host_type(True):
        # Watcom defaults to the root folder
        home_drive = os.getenv("HOMEDRIVE", "C:")
        watcom_path = convert_from_windows_path(home_drive + "\\WATCOM")
        full_paths.append(watcom_path)

        # Try the "ProgramFiles" folders
        for item in _WINDOWS_ENV_PATHS:
            if os.getenv(item, None):
                watcom_path = os.path.expandvars("${" + item + "}\\watcom")
                watcom_path = convert_from_windows_path(watcom_path)
                full_paths.append(watcom_path)

    if IS_LINUX:
        # Posix / Linux
        full_paths.append("/usr/bin/watcom")

    # Scan the list of known locations
    for watcom_path in full_paths:
        # Valid?
        full_path = os.path.join(watcom_path, exe_folder, fake_command)
        if is_exe(os.path.join(watcom_path, full_path)):
            # Finally found it!
            _WATCOM_PATH = watcom_path
            return full_path if command else watcom_path

    # Oh, dear.
    if verbose:
        print("Watcom was not found!")

    # Can't find it
    return None

########################################


def _get_doxygen_registry_path():
    """
    Locate doxygen path using the Window Registry

    Private function only called on Windows hosts to query the registry for the
    location of Doxygen.

    Check HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\
        doxygen_is1 for the base directory of Doxygen on Windows.

    Returns:
        None or a string with the path to CodeBlocks
    """

    # Open the registry key
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE,
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\doxygen_is1",
            0, KEY_READ)
    except FileNotFoundError:
        return None

    # If a key was found, get the path
    doxygen_path, _ = QueryValueEx(key, "InstallLocation")
    CloseKey(key)

    # Convert to path
    doxygen_path = convert_to_windows_slashes(
        doxygen_path, True) + "bin\\doxygen.exe"

    # Convert to Linux/Windows/Cygwin
    return convert_from_windows_path(doxygen_path)

########################################


def where_is_doxygen(verbose=False, refresh=False, path=None):
    """
    Return the location of Doxygen's executable

    Look for an environment variable DOXYGEN and determine if the executable
    resides there. Otherwise traverse the path to see if doxygen is present.
    If that fails, look in the registry, or the usual locations like
    "Program Files\\doxygen" on Windows.

    If running on a MacOSX client, look in the Applications folder for a copy of
    Doxygen.app and return the pathname to the copy of doxygen that resides
    within.

    Args:
        verbose: If True, print a message if doxygen was not found
        refresh: If True, reset the cache and force a reload.
        path: Path to doxygen to place in the cache

    Returns:
        A path to the Doxygen command line executable or None if not found.

    """

    # pylint: disable=global-statement
    # pylint: disable=too-many-branches

    global _DOXYGEN_PATH

    # Clear the cache if needed
    if refresh:
        _DOXYGEN_PATH = None

    # Set the override, if found
    if path:
        _DOXYGEN_PATH = path

    # Is cached?
    if _DOXYGEN_PATH:
        return _DOXYGEN_PATH

    # Try the environment variable first
    if os.getenv("DOXYGEN", None):
        if get_windows_host_type(True):

            # Windows points to the base path
            doxygenpath = os.path.expandvars("${DOXYGEN}\\bin\\doxygen.exe")
            doxygenpath = convert_from_windows_path(doxygenpath)
        else:
            # Just append the exec name
            doxygenpath = os.path.expandvars("${DOXYGEN}/doxygen")

        # Valid?
        if is_exe(doxygenpath):
            _DOXYGEN_PATH = doxygenpath
            return doxygenpath

    # Scan the PATH for the exec
    doxygenpath = find_in_path("doxygen", executable=True)
    if doxygenpath:
        _DOXYGEN_PATH = doxygenpath
        return doxygenpath

    # List of the usual suspects
    full_paths = []

    # Check if it's installed but not in the path
    if get_windows_host_type(True):

        # Check the registry
        doxygen_path = _get_doxygen_registry_path()
        if doxygen_path:
            full_paths.append(doxygen_path)

        # Try the "ProgramFiles" folders
        for item in _WINDOWS_ENV_PATHS:
            if os.getenv(item, None):
                doxygen_path = os.path.expandvars(
                    "${" + item + "}\\doxygen\\bin\\doxygen.exe")
                doxygenpath = convert_from_windows_path(doxygen_path)
                full_paths.append(doxygen_path)

    elif get_mac_host_type():

        # MacOSX has it hidden in the application
        full_paths.append(
            "/Applications/Doxygen.app/Contents/Resources/doxygen")
        full_paths.append("/opt/local/bin/doxygen")

    if IS_LINUX:
        # Posix / Linux
        full_paths.append("/usr/bin/doxygen")

    # Scan the list of known locations
    for doxygen_path in full_paths:
        if is_exe(doxygen_path):
            # Finally found it!
            _DOXYGEN_PATH = doxygen_path
            return doxygen_path

    # Oh, dear.
    if verbose:
        print("Doxygen not found!")
        if get_mac_host_type():
            print(
                "Install the desktop application in the Applications folder "
                "or use brew or macports for the command line version")

    # Can't find it
    return None

########################################


def where_is_visual_studio(vs_version, tool_name=None, cpu=None):
    """
    Locate devenv.com for a specific version of Visual Studio.

    Given a specific version by year, check for the appropriate environment
    variable that contains the path to the executable of the IDE

    Note:
        This function will always return None on non-windows hosts.

    Examples:
        >>> burger.where_is_visual_studio(2010)
        "C:\\Program Files (x86)\\Microsoft Visual Studio 10.0"
        "\\Common7\\ide\\devenv.com"

    Args:
        vs_version: Version year as number
        tool_name: Return the path to this tool, None becomes ``devenv.com``
        cpu: String of the cpu type of the tool requested, ``x86``, ``x64``

    Returns:
        Path to devenv.com for the IDE or None.
    """

    # pylint: disable=too-many-branches

    # Test if running on a windows host
    host_type = get_windows_host_type(True)
    if not host_type:
        return None

    # Check if the version is even in the table
    table_item = _VS_TABLE.get(vs_version, None)
    if not table_item:
        return None

    # Tool to locate, use default if not supplied
    if not tool_name:
        tool_name = "devenv.com"

    # Table of cputypes to check
    cputable = []

    # Only check this one
    if cpu:
        cputable.append(cpu)

    else:
        # If already x86, or .com skip extra cpus
        if host_type != "x86" and not tool_name.endswith(".com"):

            # Prioritize the native CPU
            cputable.append(host_type)

            # If ARM, allow x64 for the emulation layer
            if host_type in ("arm", "arm64"):
                cputable.append("x64")

        # Always use x86
        cputable.append("x86")

    # Try the registry first
    for item in find_visual_studios():

        # Is this the version of Visual Studio requested?
        if item.version_info[0] == table_item[2]:

            # Check with CPUs and find a match
            for i in cputable:
                vstudiopath = item.known_paths.get(tool_name + "_" + i, None)
                if vstudiopath:
                    return vstudiopath

    # Try the environment variable next
    vstudio_paths = []
    vstudiopath = os.getenv(table_item[0], default=None)
    if vstudiopath:
        vstudio_paths.append(vstudiopath)

    # Test if this is VS 2017 or higher
    xxx = table_item[1].endswith("xxx")

    # Try the pathname next
    for program_files in _WINDOWS_ENV_PATHS:

        # Generate the proper path to test
        vstudiopath = os.getenv(program_files, None)
        if vstudiopath:

            # Has variants? Call the TVA.
            if xxx:
                for item in _VS_VARIANTS:
                    vstudio_paths.append(
                        vstudiopath +
                        "\\" +
                        table_item[1].replace("xxx", item) +
                        "\\Common7\\Tools\\")
            else:
                vstudio_paths.append(
                    vstudiopath +
                    "\\" +
                    table_item[1] +
                    "\\Common7\\Tools\\")

    for item in vstudio_paths:
        vstudiopath = convert_from_windows_path(item)

        # Locate the launcher
        vstudiopath = os.path.dirname(os.path.abspath(vstudiopath))
        vstudiopath = os.path.join(vstudiopath, "ide", tool_name)
        if os.path.isfile(vstudiopath):
            # Return the path if the file was found
            return vstudiopath

    # Give up
    return None
