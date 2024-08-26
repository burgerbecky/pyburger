#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains xcode helper functions

Functions to locate xcode and issue rez commands

@package burger.xcode

@var burger.xcode._CODEWARRIOR_LOCATIONS
Locations of CodeWarrior 9 or 10
"""

# pylint: disable=consider-using-f-string

from __future__ import absolute_import, print_function, unicode_literals

import os

from .strutils import PY3_4_OR_HIGHER, get_mac_host_type, convert_to_array
from .buildutils import run_command

# Locations of where Codewarrior is installed
_CODEWARRIOR_LOCATIONS = (
    "/Applications/Metrowerks CodeWarrior 10.0",
    "/Applications/Metrowerks CodeWarrior 9.0"
)

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


def find_rez_headers():
    """
    Locate where the resource headers are located

    Of course Apple would not be consistent where the SDKs and headers are
    located, so search for them.

    If successful, a tuple is returned with the folder to pass to ``rez`` as
    the folder that has the *.r headers as the first entry.

    If running on on Xcode 5 or higher, the SDKs is built into the app and
    the ``FlatCarbon`` headers are missing. As a result, the second entry of
    the tuple will be ``True`` to denote that Frameworks should be used instead
    of classic MacOS 9 flat header folders. If classic headers, the second
    entry of the tuple is ``False``

    Returns:
        (Path to the rez headers, True/False) or None
    """

    # Only valid on mac hosts
    if not get_mac_host_type():
        return None

    # Step 1, see if CodeWarrior is installed. If so,
    # stick to the classics

    for item in _CODEWARRIOR_LOCATIONS:

        # Located?
        if os.path.isdir(item):

            # Create the path and exit
            return (os.path.join(
                item,
                "Metrowerks CodeWarrior",
                "MacOS Support",
                "Universal",
                "Interfaces",
                "RIncludes"
            ), False)

    # At this point, look for the includes in Xcode
    xcode_ref = where_is_xcode()
    if not xcode_ref:
        # XCode not found
        return None

    # Get the directory and Xcode version
    xcode_dir = xcode_ref[0]
    # xcode_version = xcode_ref[1]

    # Remove usr/bin/xcodebuild
    xcode_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(xcode_dir)))

    # Are we a really old version of Xcode, like
    # 2, 3, or 4?
    if xcode_dir.startswith("/Developer"):

        # Go to the base directory of the SDKs
        xcode_dir = os.path.join(xcode_dir, "SDKs")

        # Since there's no hard link to the default, manually iterate
        # over the possible choices

        # Reverse sort to get the most recent first
        for item in sorted(os.listdir(xcode_dir), reverse=True):

            # Skip files, and use the first one hit
            if os.path.isdir(os.path.join(xcode_dir, item)):

                # Classic Xcode has a flattened folder for headers
                # so classic paths still work
                return (os.path.join(
                    xcode_dir,
                    item,
                    "Developer",
                    "Headers",
                    "FlatCarbon"), False)

        # No sdks installed?
        return None

    # We are a modern version of Xcode, which
    # means the SDKs are inside the app.

    # Append the path, seriously, this is the path
    # No, seriously, what were they smoking?
    return (os.path.join(
        xcode_dir,
        "Platforms",
        "MacOSX.platform",
        "Developer",
        "SDKs",
        # Use the default sdk
        "MacOSX.sdk"), True)

########################################


def build_rez(working_directory, input_file,
              output_file, creator=None, filetype=None,
              frameworks=None):
    """
    Process the Rez file using the rez tool

    Determine where the ``rez`` tool resides, as well as the MacOS rez headers.

    Runs the ``rez`` tool with the header directory properly preset. Will also
    set the creator and filetype if they are passed with 4 character strings.

    Modern versions of XCode allows the invokation of specific frameworks, pass
    them in in the frameworks parameter. It accepts a single string or an
    iterable of strings.

    Note:
        Only runs on a Mac

    Args:
        working_directory
            Directory this script resides in.

        input_file
            Name of the .r file to compile with rez

        output_file
            Name of the output file

        creator
            4 character string for the creator code

        filetype
            4 character string for the filetype

        frameworks
            iterable of frameworks that would be invoked on modern xcode

    Returns:
        Zero on success, non zero on error
    """

    # Only valid on mac hosts
    if not get_mac_host_type():
        return 10

    # Are the resource headers present?
    rez_ref = find_rez_headers()
    if rez_ref is None:
        return 10

    # Get the directory and the style
    rez_dir = rez_ref[0]
    new_style = rez_ref[1]

    # Invoke the rez compiler
    cmd = ["rez"]

    # Classic style?
    if not new_style:

        # Rez supports file creator and type so set them if needed
        if creator:
            cmd.append("-c")
            cmd.append(creator)

        if filetype:
            cmd.append("-t")
            cmd.append(filetype)

        # Location of resource headers
        cmd.append("-i")
        cmd.append(rez_dir)
    else:
        # New style means using frameworks

        # Alert the source file that frameworks are in play
        cmd.append("-d")
        cmd.append("USING_FRAMEWORKS")

        # Location of the sdk
        cmd.append("-is")
        cmd.append(rez_dir)

        # Use these frameworks
        if frameworks:
            for item in convert_to_array(frameworks):
                cmd.append("-F")
                cmd.append(item)

    # Append output name
    cmd.append("-o")
    cmd.append(output_file)

    # Append the input name
    cmd.append(input_file)

    # Run the compiler
    error, _, _ = run_command(cmd, working_directory)

    if not error and new_style:
        # New style Rez generator doesn't set the filetype or creator

        # Do it manually if needed
        if creator or filetype:
            cmd = ["SetFile"]

            if creator:
                cmd.append("-c")
                cmd.append(creator)

            if filetype:
                cmd.append("-t")
                cmd.append(filetype)

            cmd.append(output_file)

            error, _, _ = run_command(cmd, working_directory)

    # Return the error code
    return error
