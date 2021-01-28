#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains windows only functions
"""

## \package burger._find_visual_studio

from __future__ import absolute_import, print_function, unicode_literals

import os.path

from ._vsinstance import VisualStudioInstance

try:
    from wslwinreg import convert_from_windows_path, get_file_info
except ImportError:
    pass

# pylint: disable=useless-object-inheritance
# pylint: disable=too-many-arguments
# pylint: disable=unnecessary-pass
# pylint: disable=too-few-public-methods

## List of Visual Studio tools
_VSTOOLS = ('cl.exe', 'link.exe', 'lib.exe')

## List of IDE tools
_IDETOOLS = ('devenv.exe', )

## Versions of Visual Studio from 2003 to 2015
_VSVERSIONS = ('7.1', '8.0', '9.0', '10.0', '11.0', '12.0', '14.0')

## List of supported CPUs for Visual Studio  tools
_SUPPORTED_CPUS = ('x86', 'x64', 'arm', 'arm64')

########################################


def _find_vs2003_2015(installed_roots):
    """
    Find all versions of Visual Studio from 2003 to 2015.

    Args:
        installed_roots: Open registry key 'Software\\Microsoft'
    """

    # pylint: disable=too-many-branches
    result_list = []

    for key in _VSVERSIONS:

        known_paths = {}

        # Get the root pathname to the Visual Studio version
        try:
            sub_key = installed_roots.open_subkey('VisualStudio\\SxS\\VS7')
            vs_path = convert_from_windows_path(
                sub_key.get_value(key)[0])
        except OSError:
            continue

        # Locate devenv.exe and related files
        for item in _IDETOOLS:
            test_dir = os.path.join(
                vs_path, 'Common7', 'IDE', item)
            if os.path.exists(test_dir):
                known_paths[item + '_x86'] = test_dir

        # vcvarsall.bat is a special case
        if key == '7.1':
            test_dir = os.path.join(vs_path, 'Common7', 'Tools', 'vsvars32.bat')
            if os.path.exists(test_dir):
                known_paths['vcvarsall.bat'] = test_dir

        # Get the pathname to the Visual Studio tools
        try:
            sub_key = installed_roots.open_subkey('VisualStudio\\SxS\\VC7')
            vc7_path = convert_from_windows_path(
                sub_key.get_value(key)[0])
        except OSError:
            continue

        # vcvarsall.bat is a special case
        if key != '7.1':
            test_dir = os.path.join(vc7_path, 'vcvarsall.bat')
            if os.path.exists(test_dir):
                known_paths['vcvarsall.bat'] = test_dir

        # Locate the compiler and linkers
        for item in _VSTOOLS:
            test_dir = os.path.join(vc7_path, 'bin', item)
            if os.path.exists(test_dir):
                known_paths[item + '_x86'] = test_dir

        # Locate msbuild, if available. VS 2013 and higher.
        try:
            sub_key = installed_roots.open_subkey(
                'MSBuild\\ToolsVersions\\' + key)
            vc7_path = convert_from_windows_path(
                sub_key.get_value('MSBuildToolsPath')[0])
        except OSError:
            vc7_path = None

        # Is there an MSBuild toolchain?
        if vc7_path:
            test_dir = os.path.join(vc7_path, 'msbuild.exe')
            if os.path.exists(test_dir):
                known_paths['msbuild.exe' + '_x86'] = test_dir

        version_number = get_file_info(
            known_paths['devenv.exe_x86'], 'ProductVersion')
        file_description = get_file_info(
            known_paths['devenv.exe_x86'], 'FileDescription')
        result_list.append(VisualStudioInstance(
            file_description,
            version_number,
            vs_path,
            known_paths
        ))

    return result_list

########################################


def _find_vs2017_higher(installed_roots):
    """
    Find all versions of Visual Studio 2017 and higher.

    Args:
        installed_roots: Open registry key 'Software\\Microsoft'
    """

    # pylint: disable=too-many-branches
    result_list = []

    # Scan registery keys for VisualStudio_*
    for key in installed_roots.get_subkeys():

        if not key.startswith('VisualStudio_'):
            continue

        # Found an installed copy of Visual Studio
        known_paths = {}

        # Get the root pathname to the Visual Studio version
        try:
            sub_key = installed_roots.open_subkey(key + '\\Capabilities')
            vs_path = sub_key.get_value('ApplicationDescription')[0]
        except OSError:
            continue

        # Get rid of extra characters
        vs_path = convert_from_windows_path(
            vs_path.lstrip('@').rsplit(',', 1)[0])
        vs_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(vs_path)))

        # Locate devenv.exe and related files
        for item in _IDETOOLS:
            test_dir = os.path.join(
                vs_path, 'Common7', 'IDE', item)
            if os.path.exists(test_dir):
                known_paths[item + '_x86'] = test_dir

        # vcvarsall.bat is a special case
        test_dir = os.path.join(
            vs_path,
            'VC',
            'Auxiliary',
            'Build',
            'vcvarsall.bat')
        if os.path.exists(test_dir):
            known_paths['vcvarsall.bat'] = test_dir

        version_number = get_file_info(
            known_paths['devenv.exe_x86'], 'ProductVersion')
        file_description = get_file_info(
            known_paths['devenv.exe_x86'], 'FileDescription')

        # Locate msbuild
        test_dir = os.path.join(
            vs_path,
            'MSBuild',
            version_number.split('.')[0] + '.0',
            'Bin',
            'MSBuild.exe')
        if os.path.exists(test_dir):
            known_paths['msbuild.exe' + '_x86'] = test_dir
        else:
            test_dir = os.path.join(
                vs_path,
                'MSBuild',
                'Current',
                'Bin',
                'MSBuild.exe')
            if os.path.exists(test_dir):
                known_paths['msbuild.exe' + '_x86'] = test_dir
        result_list.append(VisualStudioInstance(
            file_description,
            version_number,
            vs_path,
            known_paths
        ))

    return result_list
