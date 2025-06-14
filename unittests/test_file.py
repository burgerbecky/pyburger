#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger file functions

Copyright 2013-2025 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

# pylint: disable=wrong-import-position
# pylint: disable=too-many-statements
# pylint: disable=redundant-u-string-prefix
# pylint: disable=unspecified-encoding

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
import unittest
import tempfile
import shutil
import filecmp

# Insert the location of burger at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import burger

CRLF_TESTS = [
    "testing 1",
    "testing 2",
    "testing 3"
]

# Bishojou Senshi Sailor Moon
SENSHI = u"\u7f8e\u5c11\u5973\u6226\u58eb\u30bb\u30fc\u30e9" \
    "\u30fc\u30e0\u30fc\u30f3"

########################################


class TestFile(unittest.TestCase):
    """
    Test the file functions
    """

    def setUp(self):
        """
        Handle temporary directory
        """
        self.saved_cwd = os.getcwd()
        self.tmpdir = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmpdir)

########################################

    def tearDown(self):
        """
        Restore directory
        """
        os.chdir(self.saved_cwd)

########################################

    def test_traverse_directory(self):
        """
        Test burger.traverse_directory()
        """

        # Files to scan for
        fooey1 = "foo1.txt"
        fooey2 = "foo2.txt"

        # Create the folder a/b/c/d
        dir1 = self.tmpdir
        dir2 = os.path.join(dir1, "a")
        dir3 = os.path.join(dir2, "b")
        dir4 = os.path.join(dir3, "c")
        dir5 = os.path.join(dir4, "d")
        os.makedirs(dir5)

        # Perform tests that result in empty lists
        temp_list = burger.traverse_directory(dir5, fooey1, False)
        self.assertFalse(temp_list)
        temp_list = burger.traverse_directory(
            dir5, (fooey1, fooey2), False)
        self.assertFalse(temp_list)
        temp_list = burger.traverse_directory(
            dir5, [fooey1, fooey2], False)
        self.assertFalse(temp_list)
        temp_list = burger.traverse_directory(
            dir5, {fooey1, fooey2}, False)
        self.assertFalse(temp_list)

        # Add some files
        fooey1path = os.path.join(dir2, fooey1)
        fooey2path = os.path.join(dir4, fooey2)
        with open(fooey1path, "w") as text_file:
            text_file.write(fooey1)
        with open(fooey2path, "w") as text_file:
            text_file.write(fooey2)

        # Verify these files are found
        temp_list = burger.traverse_directory(dir5, fooey1, False)
        self.assertEqual(temp_list, [fooey1path])

        temp_list = burger.traverse_directory(dir5, fooey2, False)
        self.assertEqual(temp_list, [fooey2path])

        # Perform tests that result in empty lists
        check_list = [fooey1path, fooey2path]
        temp_list = burger.traverse_directory(
            dir5, (fooey1, fooey2), False)
        self.assertEqual(temp_list, check_list)
        temp_list = burger.traverse_directory(
            dir5, [fooey1, fooey2], False)
        self.assertEqual(temp_list, check_list)
        temp_list = burger.traverse_directory(
            dir5, {fooey1, fooey2}, False)
        self.assertEqual(temp_list, check_list)

        # Add some more files
        fooey1path2 = os.path.join(dir1, fooey1)
        fooey2path2 = os.path.join(dir5, fooey2)
        with open(fooey1path2, "w") as text_file:
            text_file.write(fooey1)
        with open(fooey2path2, "w") as text_file:
            text_file.write(fooey2)

        # Verify these files are found
        temp_list = burger.traverse_directory(dir5, fooey1, False)
        self.assertEqual(temp_list, [fooey1path2, fooey1path])

        temp_list = burger.traverse_directory(dir5, fooey2, False)
        self.assertEqual(temp_list, [fooey2path, fooey2path2])

        # Perform tests that result in empty lists
        check_list = [fooey1path2, fooey1path, fooey2path, fooey2path2]
        temp_list = burger.traverse_directory(
            dir5, (fooey1, fooey2), False)
        self.assertEqual(temp_list, check_list)
        temp_list = burger.traverse_directory(
            dir5, [fooey1, fooey2], False)
        self.assertEqual(temp_list, check_list)
        temp_list = burger.traverse_directory(
            dir5, {fooey1, fooey2}, False)
        self.assertEqual(temp_list, check_list)


########################################


    def test_load_text_file(self):
        """
        Test burger.load_text_file()
        """

        selffile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

        # Using hard coded test files, ensure all load fine
        self.assertEqual(
            burger.load_text_file(
                os.path.join(
                    selffile,
                    "lf.txt")),
            CRLF_TESTS)
        self.assertEqual(
            burger.load_text_file(
                os.path.join(
                    selffile,
                    "cr.txt")),
            CRLF_TESTS)
        self.assertEqual(burger.load_text_file(
            os.path.join(
                selffile,
                "crlf.txt")), CRLF_TESTS)

        # Test reading utf-8 with BOM
        self.assertEqual(burger.load_text_file(
            os.path.join(
                selffile,
                "senshi.txt")), [SENSHI])

########################################

    def test_save_text_file(self):
        """
        Test burger.save_text_file()
        """

        burger.save_text_file(os.path.join(self.tmpdir, "lf.txt"),
                            CRLF_TESTS, "\n")
        burger.save_text_file(os.path.join(self.tmpdir, "cr.txt"),
                            CRLF_TESTS, "\r")
        burger.save_text_file(os.path.join(self.tmpdir, "crlf.txt"),
                            CRLF_TESTS, "\r\n")
        burger.save_text_file(os.path.join(self.tmpdir, "senshi.txt"),
                            SENSHI, bom=True)

        selffile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

        # Test writing all the line feeds
        self.assertTrue(filecmp.cmp(os.path.join(selffile, "lf.txt"),
                        os.path.join(self.tmpdir, "lf.txt")))
        self.assertTrue(filecmp.cmp(os.path.join(selffile, "cr.txt"),
                        os.path.join(self.tmpdir, "cr.txt")))
        self.assertTrue(filecmp.cmp(os.path.join(selffile, "crlf.txt"),
                        os.path.join(self.tmpdir, "crlf.txt")))

        # Try UTF-8 with BOM
        self.assertTrue(filecmp.cmp(os.path.join(selffile, "senshi.txt"),
                        os.path.join(self.tmpdir, "senshi.txt")))

########################################

    def test_compare_files(self):
        """
        Test burger.compare_files()
        """

        selffile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

        # Test writing all the line feeds
        self.assertTrue(burger.compare_files(os.path.join(selffile, "lf.txt"),
                                    os.path.join(selffile, "cr.txt")))
        self.assertTrue(burger.compare_files(os.path.join(selffile, "lf.txt"),
                                    os.path.join(selffile, "crlf.txt")))
        self.assertTrue(burger.compare_files(os.path.join(selffile, "cr.txt"),
                                    os.path.join(selffile, "crlf.txt")))

        # Intentional mismatch
        self.assertFalse(burger.compare_files(
            os.path.join(
                selffile, "lf.txt"), os.path.join(
                selffile, "senshi.txt")))

        # Test for missing files
        self.assertFalse(burger.compare_files(os.path.join(selffile, "llf.txt"),
                                    os.path.join(selffile, "cr.txt")))
        self.assertFalse(burger.compare_files(os.path.join(selffile, "lf.txt"),
                                    os.path.join(selffile, "lcr.txt")))

########################################

    def test_compare_file_to_string(self):
        """
        Test burger.compare_file_to_string()
        """

        selffile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

        # Test writing all the line feeds
        self.assertTrue(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "lf.txt"),
                CRLF_TESTS))

        self.assertTrue(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "cr.txt"),
                CRLF_TESTS))

        self.assertTrue(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "crlf.txt"),
                CRLF_TESTS))

        # Test against single string with line feeds
        self.assertTrue(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "crlf.txt"),
                "\n".join(CRLF_TESTS)))

        self.assertTrue(burger.compare_file_to_string(
            os.path.join(selffile, "senshi.txt"), SENSHI))

        # Intentional mismatch
        self.assertFalse(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "lf.txt"),
                [SENSHI]))

        # Test for missing files
        self.assertFalse(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "llf.txt"),
                CRLF_TESTS))

        self.assertFalse(
            burger.compare_file_to_string(
                os.path.join(
                    selffile,
                    "lf.txt"),
                None))

########################################

    def test_read_zero_terminated_str(self):
        """
        Test burger.read_zero_terminated_string()
        """

        selffile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data")

        with open(os.path.join(selffile, "zeroterminate.bin"), "rb") as filep:

            # Test ascii
            for item in CRLF_TESTS:
                self.assertEqual(
                    burger.read_zero_terminated_string(filep), item)

            # Test Japanese utf-8
            self.assertEqual(burger.read_zero_terminated_string(filep), SENSHI)

            # Test Windows
            self.assertEqual(
                burger.read_zero_terminated_string(
                    filep,
                    encoding="cp1252"),
                u"\u2018\u2019\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5")

            # Test ISO-8859-1
            self.assertEqual(
                burger.read_zero_terminated_string(
                    filep,
                    encoding="latin_1"),
                u"\u0091\u0092\u00C0\u00C1\u00C2\u00C3\u00C4\u00C5")

            # Test MacRoman
            self.assertEqual(
                burger.read_zero_terminated_string(
                    filep,
                    encoding="mac_roman"),
                u"\u00EB\u00ED\u00BF\u00A1\u00AC\u221A\u0192\u2248")

            # Test empty string
            self.assertEqual(burger.read_zero_terminated_string(filep), "")

            # Test EOF
            self.assertIsNone(burger.read_zero_terminated_string(filep))


########################################


if __name__ == "__main__":
    unittest.main()
