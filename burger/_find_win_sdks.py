#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that locates all Windows SDKs.
"""

## \package burger._find_win_sdks

from __future__ import absolute_import, print_function, unicode_literals

import os.path

from ._vsinstance import WindowsSDKInstance

try:
    from wslwinreg import convert_from_windows_path
except ImportError:
    pass

from .strutils import make_version_tuple

# pylint: disable=useless-object-inheritance
# pylint: disable=too-many-arguments
# pylint: disable=unnecessary-pass
# pylint: disable=too-few-public-methods

########################################

## List of Windows 5 SDK registry keys
_WIN5_KEYS = (('7.1', '5.0'), ('8.0', '5.1'))

## List of Windows 6-7 SDK registry keys
_WIN6_7_KEYS = ('v6.0A', 'v7.0A', 'v7.1A')

## List of supported CPUs for Windows 6-7 SDKs
_WIN6_7SDK_CPUS = ('x86', 'x64')

## List of Windows 8 SDK registry keys
_WIN8_KEYS = (('KitsRoot', '8.0'), ('KitsRoot81', '8.1'))

## List of supported CPUs for Windows 8 SDKs
_WIN8SDK_CPUS = ('x86', 'x64', 'arm')

## List of header folders
_WIN8SDK_HEADER_FOLDERS = ('um', 'shared', 'winrt')

## List of library folders
_WIN8SDK_LIB_FOLDERS = (('win8', 'um'), ('winv6.3', 'um'))

## List of supported CPUs for Windows 10 SDKs
_WIN10SDK_CPUS = ('x86', 'x64', 'arm', 'arm64')

## List of header folders
_WIN10SDK_HEADER_FOLDERS = ('ucrt', 'um', 'shared', 'winrt', 'cppwinrt')

## List of library folders
_WIN10SDK_LIB_FOLDERS = ('ucrt', 'um')

## List of executables
_WIN10_EXECS = ('rc.exe', 'signtool.exe', 'makecat.exe', 'midl.exe', 'mc.exe')

########################################


def _find_windows5_sdks(installed_roots):
    """
    Scan the system for all copies of the Windows 5 SDKs

    Windows 5 is Windows XP.

    The SDKs are found by looking at the registry key
    Software\\Microsoft\\Microsoft SDKs\\Windows

    Args:
        installed_roots: Open registry key 'Software\\Microsoft'

    Returns:
        List of WindowsSDKInstance for every version of the Windows 6 and 7
        SDK found.
    """

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-nested-blocks

    # Nothing found
    result_list = []

    try:
        key_vc7 = installed_roots.open_subkey(
            'VisualStudio\\SxS\\VC7')
    except OSError:
        return result_list

    # Get the master key, if present
    for key, version_number in _WIN5_KEYS:

        # Get the pathname to the Windows 10 kits, if present.
        try:
            windows_5_path = convert_from_windows_path(
                key_vc7.get_value(key)[0])
        except OSError:
            continue

        windows_5_path = windows_5_path.rstrip('\\/')
        # Initialize the path directory
        known_paths = {}

        # Find the header folder
        test_dir = os.path.join(windows_5_path, 'PlatformSDK', 'Include')
        if os.path.exists(test_dir):
            known_paths['WinSDK.um'] = test_dir

        # Find all the library folders
        # Note, x86 is assumes, x64 is a sub folder
        for cpu in _WIN6_7SDK_CPUS:
            test_dir = os.path.join(windows_5_path, 'PlatformSDK',
                'Lib', '' if cpu == 'x86' else 'AMD64')
            if os.path.exists(test_dir):
                suffix = '_' + cpu
                known_paths['WinSDK.lib' + suffix] = test_dir

        # Find all executables
        for item in _WIN10_EXECS:
            for cpu in _WIN6_7SDK_CPUS:
                # Try the AMD64 path only
                test_dir = os.path.join(
                    windows_5_path, 'PlatformSDK',
                    'bin',
                    '' if cpu == 'x86' else 'win64' +
                    os.path.sep +
                    'AMD64',
                    item)
                if os.path.exists(test_dir):
                    known_paths[item + '_' + cpu] = test_dir

                # The x86 version has other paths for where the
                # tools are located, because, of course they are.
                elif cpu == 'x86':

                    # Try without PlatformSDK
                    test_dir = os.path.join(
                        windows_5_path, 'bin', item)
                    if os.path.exists(test_dir):
                        known_paths[item + '_' + cpu] = test_dir
                    else:
                        test_dir = os.path.join(
                            os.path.dirname(windows_5_path),
                            'Common7', 'Tools', 'Bin', item)
                        if os.path.exists(test_dir):
                            known_paths[item + '_' + cpu] = test_dir

        result_list.append(WindowsSDKInstance(
            'Windows {} SDK'.format(version_number[0]),
            version_number,
            windows_5_path,
            known_paths
        ))

    return result_list

########################################


def _find_windows6_7_sdks(installed_roots):
    """
    Scan the system for all copies of the Windows 6 and 7 SDKs

    Windows 6 is Vista, Windows 7 is.. well, you know.

    The SDKs are found by looking at the registry key
    Software\\Microsoft\\Microsoft SDKs\\Windows

    Args:
        installed_roots: Open registry key 'Software\\Microsoft'

    Returns:
        List of WindowsSDKInstance for every version of the Windows 6 and 7
        SDK found.
    """

    # pylint: disable=too-many-branches

    # Nothing found
    result_list = []

    try:
        key_sdks = installed_roots.open_subkey(
            'Microsoft SDKs\\Windows')
    except OSError:
        return result_list

    # Get the master key, if present
    for key in _WIN6_7_KEYS:

        # Get the pathname to the Windows 10 kits, if present.
        try:
            sub_key = key_sdks.open_subkey(key)
            windows_6_7_path = convert_from_windows_path(
                sub_key.get_value('InstallationFolder')[0])
        except OSError:
            continue

        try:
            version_number = sub_key.get_value('ProductVersion')[0]
        except OSError:
            continue

        # This hack is to get the version number of the Windows v6.0A
        # SDK because it hides it in one of two sub keys

        # Check if the version starts with 'v' (Broken v6.0)
        if version_number[0] == 'v':
            try:
                # Try to extract it from the VistaClientWin32Tools subkey
                version_number = sub_key.open_subkey(
                    'VistaClientWin32Tools').get_value('ProductVersion')[0]
            except OSError:
                try:
                    # Try again
                    version_number = sub_key.open_subkey(
                        'VistaClientSDKTools').get_value('ProductVersion')[0]
                except OSError:
                    # Give up and just remove the leading 'v'
                    version_number = version_number[1:]
                    continue

        # Initialize the path directory
        known_paths = {}

        # Find the header folder
        test_dir = os.path.join(windows_6_7_path, 'Include')
        if os.path.exists(test_dir):
            known_paths['WinSDK.um'] = test_dir

        # Find all the library folders
        # Note, x86 is assumes, x64 is a sub folder
        for cpu in _WIN6_7SDK_CPUS:
            test_dir = os.path.join(windows_6_7_path,
                'Lib', cpu if cpu != 'x86' else '')
            if os.path.exists(test_dir):
                suffix = '_' + cpu
                known_paths['WinSDK.lib' + suffix] = test_dir

        # Find all executables
        for item in _WIN10_EXECS:
            for cpu in _WIN6_7SDK_CPUS:
                test_dir = os.path.join(windows_6_7_path,
                        'bin', cpu if cpu != 'x86' else '', item)
                if os.path.exists(test_dir):
                    known_paths[item + '_' + cpu] = test_dir

        result_list.append(WindowsSDKInstance(
            'Windows {} SDK'.format(version_number[0]),
            version_number,
            windows_6_7_path,
            known_paths
        ))

    return result_list

########################################


def _find_windows8_sdks(installed_roots):
    """
    Scan the system for all copies of the Windows 8 SDKs

    The SDKs are found by looking at the registry key
    Software\\Microsoft\\Windows Kits\\Installed Roots\\KitsRoot8
    and KitsRoot81

    Args:
        installed_roots: Open registry key 'Software\\Microsoft'

    Returns:
        List of WindowsSDKInstance for every version of the Windows 8
        SDK found.
    """

    # pylint: disable=too-many-branches

    # Nothing found
    result_list = []

    try:
        roots_key = installed_roots.open_subkey(
            'Windows Kits\\Installed Roots')
    except OSError:
        return result_list

    # Get the master key, if present
    for key, version_number in _WIN8_KEYS:

        # Get the pathname to the Windows 8 kits, if present.
        try:
            windows_8_path = convert_from_windows_path(
                roots_key.get_value(key)[0])
        except OSError:
            continue

        # Try to get the full version number
        try:
            hkey = installed_roots.open_subkey(
                'Microsoft SDKs\\Windows')
            version_number = hkey.open_subkey(
                'v{}A'.format(version_number)).get_value('ProductVersion')[0]
        except OSError:
            pass

        # Initialize the path directory
        known_paths = {}

        # Find all the header folders
        for item in _WIN8SDK_HEADER_FOLDERS:
            test_dir = os.path.join(windows_8_path,
                'Include', item)
            if os.path.exists(test_dir):
                known_paths['WinSDK.' + item] = test_dir

        # Find all the library folders
        for item, item2 in _WIN8SDK_LIB_FOLDERS:
            for cpu in _WIN8SDK_CPUS:
                test_dir = os.path.join(windows_8_path,
                    'Lib', item, item2, cpu)
                if os.path.exists(test_dir):
                    suffix = item2 if item2 != 'um' else ''
                    suffix = suffix + '_' + cpu
                    known_paths['WinSDK.lib' + suffix] = test_dir

        # Find all executables
        for item in _WIN10_EXECS:
            for cpu in _WIN8SDK_CPUS:
                test_dir = os.path.join(windows_8_path,
                        'bin', cpu, item)
                if os.path.exists(test_dir):
                    known_paths[item + '_' + cpu] = test_dir

        result_list.append(WindowsSDKInstance(
            'Windows 8 SDK',
            version_number,
            windows_8_path,
            known_paths
        ))

    return result_list

########################################


def _find_windows10_sdks(installed_roots):
    """
    Scan the system for all copies of the Windows 10 SDKs

    The SDKs are found by looking at the registry key
    Software\\Microsoft\\Windows Kits\\Installed Roots\\KitsRoot10

    Args:
        installed_roots: Open registry key 'Software\\Microsoft'

    Returns:
        List of WindowsSDKInstance for every version of the Windows 10
        SDK found.
    """

    # pylint: disable=too-many-branches

    # Nothing found
    result_list = []

    # Get the master key, if present
    try:
        roots_key = installed_roots.open_subkey(
            'Windows Kits\\Installed Roots')
    except OSError:
        return result_list

    # Get the pathname to the Windows 10 kits, if present.
    try:
        windows_10_path = convert_from_windows_path(
            roots_key.get_value('KitsRoot10')[0])
    except OSError:
        return result_list

    # Iterate over the version numbers
    for version_number in os.listdir(
            os.path.join(windows_10_path, 'Include')):
        # Convert to version tuple
        version_info = make_version_tuple(version_number)

        # Ensure it's a Windows 10 SDK
        if version_info[0] == 10:

            # Initialize the path directory
            known_paths = {}

            # Find all the header folders
            for item in _WIN10SDK_HEADER_FOLDERS:
                test_dir = os.path.join(windows_10_path,
                    'Include', version_number, item)
                if os.path.exists(test_dir):
                    known_paths['WinSDK.' + item] = test_dir

            # Find all the library folders
            for item in _WIN10SDK_LIB_FOLDERS:
                for cpu in _WIN10SDK_CPUS:
                    test_dir = os.path.join(windows_10_path,
                        'Lib', version_number, item, cpu)
                    if os.path.exists(test_dir):
                        suffix = item if item != 'um' else ''
                        suffix = suffix + '_' + cpu
                        known_paths['WinSDK.lib' + suffix] = test_dir

            # Find all executables
            for item in _WIN10_EXECS:
                for cpu in _WIN10SDK_CPUS:
                    test_dir = os.path.join(windows_10_path,
                        'bin', version_number, cpu, item)
                    if os.path.exists(test_dir):
                        known_paths[item + '_' + cpu] = test_dir
                        continue
                    test_dir = os.path.join(windows_10_path,
                            'bin', cpu, item)
                    if os.path.exists(test_dir):
                        known_paths[item + '_' + cpu] = test_dir

            result_list.append(WindowsSDKInstance(
                'Windows 10 SDK',
                version_number,
                windows_10_path,
                known_paths
            ))

    return result_list
