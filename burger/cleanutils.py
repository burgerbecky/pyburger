#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains clean helper functions
"""

## \package burger.cleanutils

from __future__ import absolute_import, print_function, unicode_literals

import os

from .fileutils import clean_files, clean_directories

########################################


def clean_xcode(path, recursive=False):
    """
    Scan for XCode project folders and perform a clean.

    Scan the current folder and for every folder that is an XCode
    project, remove all user files from the folder

    Args:
        path: Directory to begin scanning
        recursive: Boolean if recursive clean is desired

    See:
        fileutils.clean_files() and fileutils.clean_directories()
    """

    # Purging user data in XCode projects

    for item in os.listdir(path):
        file_name = os.path.join(path, item)
        if item.endswith('.xcodeproj'):
            if os.path.isdir(file_name):
                if os.path.isfile(os.path.join(file_name, 'project.pbxproj')):
                    clean_directories(
                        file_name, ('xcuserdata', 'project.xcworkspace'))
                    clean_files(file_name, ('*.mode1v3', '*.pbxuser'))
                    continue
        if recursive:
            if os.path.isdir(file_name):
                clean_xcode(file_name, recursive)
