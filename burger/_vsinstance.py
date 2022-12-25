#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package containing shared classes for Windows SDK and Visual Studio
instance searches.

@package burger._vsinstance
"""

# pylint: disable=useless-object-inheritance
# pylint: disable=consider-using-f-string

from .strutils import make_version_tuple

########################################


class VisualStudioInstance(object):
    """
    Instance of the location of Visual Studio.

    More info is here @ref md_find_visual_studio

    Attributes:
        name: Name of the Visual Studio instance or SDK
        version_string: String of the version of this SDK
        version_info: Integer tuple of self.version
        path: Root pathname of the object
        known_paths: dict of pathnames for specific items

    See Also:
        WindowsSDKInstance
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-few-public-methods

    def __init__(self, name, ver, path, known_paths):
        """
        Initialize a VisualStudioInstance

        Args:
            name: Name of the SDK or Visual Studio instance
            ver: Version string.
            path: Base path to the SDK or Visual Studio instance.
            known_paths: dir of paths for specific executables and folders.
        """

        self.name = name
        self.version_string = ver
        self.version_info = make_version_tuple(ver)
        self.path = path.rstrip("\\/")
        self.known_paths = known_paths

    def __repr__(self):
        """
        Print the name of the class instance.
        """
        return "<{} {} at {}>".format(
            type(self).__name__, self.version_string, self.path)

    def __str__(self):
        """
        Print the name of instance.
        """
        return self.name

########################################


class WindowsSDKInstance(VisualStudioInstance):
    """
    Instance of paths for a Windows SDK.

    More info is here @ref md_find_visual_studio

    See Also:
        VisualStudioInstance
    """

    # pylint: disable=unnecessary-pass
    # pylint: disable=too-few-public-methods
    pass
