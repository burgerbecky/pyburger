#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains windows only functions

They will operate on Windows, Cygwin, MSYS2 and Windows Subsystem for
Linux. On macOS and pure Linux, they will return no data.
"""

## \package burger.windowsutils

from .strutils import get_windows_host_type

from ._find_win_sdks import _find_windows5_sdks, _find_windows6_7_sdks, \
    _find_windows8_sdks, _find_windows10_sdks

from ._find_visual_studio import _find_vs2003_2015, _find_vs2017_higher

try:
    from wslwinreg import get_HKLM_32
except ImportError:
    pass

## find_visual_studios() cache
_FIND_VISUAL_STUDIOS = []

########################################


def find_visual_studios(refresh=False):
    """
    Find every Windows SDK from 5.0 and higher.

    This function may take some time if multiple copies of Visual
    Studio are installed on the machine. For speed, the results are
    cached and the cache is used on subsequent calls.

    More info is here @ref md_find_visual_studio

    Note:
        This function will return an empty list on macOS and pure Linux.
        It has been tested on Windows, Cygwin, MSYS2 and Ubuntu Windows
        Subsystem for Linux.
    Args:
        refresh: Force the cache to be reset if True.
    Returns:
        list of WindowsSDKInstance for every SDK found.
    """

    # pylint: disable=global-statement
    global _FIND_VISUAL_STUDIOS

    result_list = _FIND_VISUAL_STUDIOS
    if not result_list or refresh:
        # Self explanatory. :)

        # Nothing found
        result_list = []

        # Only works on Windows hosted platforms
        if get_windows_host_type(True):

            # Get the root registry key
            try:
                installed_roots = get_HKLM_32().open_subkey(
                    'Software\\Microsoft')
            except OSError:
                installed_roots = None

            if installed_roots:
                result_list.extend(_find_vs2003_2015(installed_roots))
                result_list.extend(_find_vs2017_higher(installed_roots))
                result_list.extend(_find_windows5_sdks(installed_roots))
                result_list.extend(_find_windows6_7_sdks(installed_roots))
                result_list.extend(_find_windows8_sdks(installed_roots))
                result_list.extend(_find_windows10_sdks(installed_roots))

        # Update the cache
        _FIND_VISUAL_STUDIOS = result_list
    return result_list
