#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains executable locators

@package burger.locators
"""

# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals

import os

from .strutils import PY3_4_OR_HIGHER, get_mac_host_type

########################################


def where_is_xcode(xcode_version=None):
    """
    Locate xcodebuild for a specific version of XCode.

    Given a specific version by version, scan the locations that the IDE
    would be found.

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
