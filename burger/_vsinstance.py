#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package containing shared classes for Windows SDK and Visual Studio
instance searches.
"""

## \package burger._vsinstance

from .strutils import make_version_tuple

########################################


# pylint: disable=useless-object-inheritance
class VisualStudioInstance(object):
    """
    Instance of the location of Visual Studio.

    More info is here @ref md_find_visual_studio

    @sa WindowsSDKInstance
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

        ## Name of the Visual Studio instance or SDK
        self.name = name

        ## String of the version of this SDK
        self.version = ver

        ## Integer tuple of self.version
        self.version_info = make_version_tuple(ver)

        ## Root pathname of the object
        self.path = path.rstrip('\\/')

        ## dict of pathnames for specific executables, headers and libraries.
        self.known_paths = known_paths

    def __repr__(self):
        """
        Print the name of the class instance.
        """
        return "<{} {} at {}>".format(
            type(self).__name__, self.version, self.path)

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

    @sa VisualStudioInstance
    """

    # pylint: disable=unnecessary-pass
    # pylint: disable=too-few-public-methods
    pass
