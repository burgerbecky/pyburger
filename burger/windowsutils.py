#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains windows only functions
"""

## \package burger.windowsutils

from ._find_win_sdks import find_windows5_sdks, find_windows6_7_sdks, \
    find_windows8_sdks, find_windows10_sdks

from ._find_visual_studio import find_vs2003_2015, find_vs2017_higher

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

    Args:
        refresh: Force the cache to be reset if True.
    Returns:
        list of WindowsSDKInstance for every SDK found.
    """

    # pylint: disable=global-statement
    global _FIND_VISUAL_STUDIOS

    result_list = _FIND_VISUAL_STUDIOS
    if not result_list or refresh:
        # Self explanitory. :)
        result_list = find_vs2003_2015()
        result_list.extend(find_vs2017_higher())
        result_list.extend(find_windows5_sdks())
        result_list.extend(find_windows6_7_sdks())
        result_list.extend(find_windows8_sdks())
        result_list.extend(find_windows10_sdks())

        # Update the cache
        _FIND_VISUAL_STUDIOS = result_list
    return result_list
