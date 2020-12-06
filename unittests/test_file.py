#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger file functions

Copyright 2013-2020 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import filecmp
import burger

CRLF_TESTS = [
    'testing 1',
    'testing 2',
    'testing 3'
]

# Bishojou Senshi Sailor Moon
SENSHI = u'\u7f8e\u5c11\u5973\u6226\u58eb\u30bb\u30fc\u30e9' \
    '\u30fc\u30e0\u30fc\u30f3'

########################################


def test_traverse_directory(tmpdir):
    """
    Test burger.traverse_directory()
    """

    # Files to scan for
    fooey1 = 'foo1.txt'
    fooey2 = 'foo2.txt'

    # Create the folder a/b/c/d
    dir1 = tmpdir
    dir2 = dir1.mkdir('a')
    dir3 = dir2.mkdir('b')
    dir4 = dir3.mkdir('c')
    dir5 = dir4.mkdir('d')

    # Perform tests that result in empty lists
    temp_list = burger.traverse_directory(str(dir5), fooey1, False)
    assert not temp_list
    temp_list = burger.traverse_directory(str(dir5), (fooey1, fooey2), False)
    assert not temp_list
    temp_list = burger.traverse_directory(str(dir5), [fooey1, fooey2], False)
    assert not temp_list
    temp_list = burger.traverse_directory(str(dir5), {fooey1, fooey2}, False)
    assert not temp_list

    # Add some files
    dir2.join(fooey1).write(fooey1)
    dir4.join(fooey2).write(fooey2)
    fooey1path = os.path.join(str(dir2), fooey1)
    fooey2path = os.path.join(str(dir4), fooey2)

    # Verify these files are found
    temp_list = burger.traverse_directory(str(dir5), fooey1, False)
    assert temp_list == [fooey1path]

    temp_list = burger.traverse_directory(str(dir5), fooey2, False)
    assert temp_list == [fooey2path]

    # Perform tests that result in empty lists
    check_list = [fooey1path, fooey2path]
    temp_list = burger.traverse_directory(str(dir5), (fooey1, fooey2), False)
    assert temp_list == check_list
    temp_list = burger.traverse_directory(str(dir5), [fooey1, fooey2], False)
    assert temp_list == check_list
    temp_list = burger.traverse_directory(str(dir5), {fooey1, fooey2}, False)
    assert temp_list == check_list

    # Add some more files
    dir1.join(fooey1).write(fooey1)
    dir5.join(fooey2).write(fooey2)
    fooey1path2 = os.path.join(str(dir1), fooey1)
    fooey2path2 = os.path.join(str(dir5), fooey2)

    # Verify these files are found
    temp_list = burger.traverse_directory(str(dir5), fooey1, False)
    assert temp_list == [fooey1path2, fooey1path]

    temp_list = burger.traverse_directory(str(dir5), fooey2, False)
    assert temp_list == [fooey2path, fooey2path2]

    # Perform tests that result in empty lists
    check_list = [fooey1path2, fooey1path, fooey2path, fooey2path2]
    temp_list = burger.traverse_directory(str(dir5), (fooey1, fooey2), False)
    assert temp_list == check_list
    temp_list = burger.traverse_directory(str(dir5), [fooey1, fooey2], False)
    assert temp_list == check_list
    temp_list = burger.traverse_directory(str(dir5), {fooey1, fooey2}, False)
    assert temp_list == check_list

    # Cleanup
    tmpdir.remove()


########################################


def test_load_text_file():
    """
    Test burger.load_text_file()
    """

    selffile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data')

    # Using hard coded test files, ensure all load fine
    assert burger.load_text_file(os.path.join(selffile, 'lf.txt')) == CRLF_TESTS
    assert burger.load_text_file(os.path.join(selffile, 'cr.txt')) == CRLF_TESTS
    assert burger.load_text_file(
        os.path.join(
            selffile,
            'crlf.txt')) == CRLF_TESTS

    # Test reading utf-8 with BOM
    assert burger.load_text_file(
        os.path.join(
            selffile,
            'senshi.txt')) == [SENSHI]

########################################


def test_save_text_file(tmpdir):
    """
    Test burger.save_text_file()
    """

    burger.save_text_file(os.path.join(str(tmpdir), 'lf.txt'),
                          CRLF_TESTS, '\n')
    burger.save_text_file(os.path.join(str(tmpdir), 'cr.txt'),
                          CRLF_TESTS, '\r')
    burger.save_text_file(os.path.join(str(tmpdir), 'crlf.txt'),
                          CRLF_TESTS, '\r\n')
    burger.save_text_file(os.path.join(str(tmpdir), 'senshi.txt'),
                          SENSHI, bom=True)

    selffile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data')

    # Test writing all the line feeds
    assert filecmp.cmp(os.path.join(selffile, 'lf.txt'),
                       os.path.join(str(tmpdir), 'lf.txt')) is True
    assert filecmp.cmp(os.path.join(selffile, 'cr.txt'),
                       os.path.join(str(tmpdir), 'cr.txt')) is True
    assert filecmp.cmp(os.path.join(selffile, 'crlf.txt'),
                       os.path.join(str(tmpdir), 'crlf.txt')) is True

    # Try UTF-8 with BOM
    assert filecmp.cmp(os.path.join(selffile, 'senshi.txt'),
                       os.path.join(str(tmpdir), 'senshi.txt')) is True

    # Cleanup
    tmpdir.remove()

########################################


def test_compare_files():
    """
    Test burger.compare_files()
    """

    selffile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data')

    # Test writing all the line feeds
    assert burger.compare_files(os.path.join(selffile, 'lf.txt'),
                                os.path.join(selffile, 'cr.txt')) is True
    assert burger.compare_files(os.path.join(selffile, 'lf.txt'),
                                os.path.join(selffile, 'crlf.txt')) is True
    assert burger.compare_files(os.path.join(selffile, 'cr.txt'),
                                os.path.join(selffile, 'crlf.txt')) is True

    # Intentional mismatch
    assert burger.compare_files(os.path.join(selffile, 'lf.txt'),
                                os.path.join(selffile, 'senshi.txt')) is False

    # Test for missing files
    assert burger.compare_files(os.path.join(selffile, 'llf.txt'),
                                os.path.join(selffile, 'cr.txt')) is False
    assert burger.compare_files(os.path.join(selffile, 'lf.txt'),
                                os.path.join(selffile, 'lcr.txt')) is False

########################################


def test_compare_file_to_string():
    """
    Test burger.compare_file_to_string()
    """

    selffile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data')

    # Test writing all the line feeds
    assert burger.compare_file_to_string(os.path.join(selffile, 'lf.txt'),
                                         CRLF_TESTS) is True
    assert burger.compare_file_to_string(os.path.join(selffile, 'cr.txt'),
                                         CRLF_TESTS) is True
    assert burger.compare_file_to_string(os.path.join(selffile, 'crlf.txt'),
                                         CRLF_TESTS) is True

    # Test against single string with line feeds
    assert burger.compare_file_to_string(os.path.join(selffile, 'crlf.txt'),
                                         '\n'.join(CRLF_TESTS)) is True
    assert burger.compare_file_to_string(os.path.join(selffile, 'senshi.txt'),
                                         SENSHI) is True

    # Intentional mismatch
    assert burger.compare_file_to_string(os.path.join(selffile, 'lf.txt'),
                                         [SENSHI]) is False

    # Test for missing files
    assert burger.compare_file_to_string(os.path.join(selffile, 'llf.txt'),
                                         CRLF_TESTS) is False
    assert burger.compare_file_to_string(os.path.join(selffile, 'lf.txt'),
                                         None) is False

########################################


def test_read_zero_terminated_str():
    """
    Test burger.read_zero_terminated_string()
    """

    selffile = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data')
    filep = open(os.path.join(selffile, 'zeroterminate.bin'), 'rb')

    # Test ascii
    for item in CRLF_TESTS:
        assert burger.read_zero_terminated_string(filep) == item

    # Test Japanese utf-8
    assert burger.read_zero_terminated_string(filep) == SENSHI
    # Test Windows
    assert burger.read_zero_terminated_string(filep, encoding='cp1252') == \
        u'\u2018\u2019\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5'
    # Test ISO-8859-1
    assert burger.read_zero_terminated_string(filep, encoding='latin_1') == \
        u'\u0091\u0092\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5'
    # Test MacRoman
    assert burger.read_zero_terminated_string(filep, encoding='mac_roman') == \
        u'\u00EB\u00ED\u00BF\u00A1\u00AC\u221A\u0192\u2248'

    # Test empty string
    assert burger.read_zero_terminated_string(filep) == ''

    # Test EOF
    assert burger.read_zero_terminated_string(filep) is None

    filep.close()
