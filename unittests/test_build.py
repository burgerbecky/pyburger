#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger file functions

Copyright 2013-2022 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

# pylint: disable=wrong-import-position

from __future__ import absolute_import, print_function, unicode_literals
import os
import sys
import unittest
import shutil
import tempfile

# Insert the location of burger at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import burger

########################################


class TestBuild(unittest.TestCase):
    """
    Test the build functions
    """

    def setUp(self):
        """
        Handle temporary directory
        """
        self.saved_cwd = os.getcwd()
        self.burger_sdks = os.getenv("BURGER_SDKS", default=None)
        self.tmpdir = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmpdir)

########################################

    def tearDown(self):
        """
        Restore directory
        """
        os.chdir(self.saved_cwd)
        if self.burger_sdks:
            os.putenv("BURGER_SDKS", self.burger_sdks)
            burger.get_sdks_folder(refresh=True, folder=self.burger_sdks)

########################################

    def test_get_sdks_folder(self):
        """
        Test burger.get_sdks_folder()
        """

        # Test with current value
        if self.burger_sdks:
            self.assertEqual(burger.get_sdks_folder(), self.burger_sdks)

        # Test folder override
        self.assertEqual(
            burger.get_sdks_folder(
                refresh=True,
                folder="test"),
            "test")
        self.assertEqual(burger.get_sdks_folder(), "test")

        # Test reading BURGER_SDKS
        os.environ["BURGER_SDKS"] = "newvalue"
        self.assertEqual(burger.get_sdks_folder(refresh=True), "newvalue")
        self.assertEqual(burger.get_sdks_folder(), "newvalue")

        # Test with fake "sdks" folder
        os.environ.pop("BURGER_SDKS", None)
        os.makedirs(os.path.join(self.tmpdir, "a", "b", "sdks", "c", "d"))
        os.chdir(os.path.join(self.tmpdir, "a", "b", "sdks", "c", "d"))
        self.assertEqual(burger.get_sdks_folder(refresh=True),
            os.path.join(self.tmpdir, "a", "b", "sdks"))

        # Restore the cache to the correct value
        if self.burger_sdks:
            os.putenv("BURGER_SDKS", self.burger_sdks)
            burger.get_sdks_folder(refresh=True, folder=self.burger_sdks)

########################################

    def test_get_path_ext(self):
        """
        Test burger.get_path_ext()
        """

        grouptuple = ("a", "b", "c", "d")
        grouplist = ["a", "b", "c", "d"]
        teststr = os.pathsep.join(grouptuple)
        self.assertEqual(burger.get_path_ext(teststr), grouplist)
        self.assertEqual(burger.get_path_ext(grouptuple), grouptuple)
        self.assertEqual(burger.get_path_ext(grouplist), grouplist)

########################################

    def test_make_exe_path(self):
        """
        Test burger.make_exe_path()
        """

        ran_test = False

        # Test for a known windows executable
        if os.getenv("SystemRoot", None):
            # Case insensitive test
            cmd = os.path.expandvars("${SystemRoot}\\System32\\cmd").lower()
            cmd_exe = cmd + ".exe"
            if os.path.isfile(cmd_exe):
                self.assertEqual(burger.make_exe_path(cmd).lower(), cmd_exe)
                ran_test = True

        # Test with ls which is in the same place on Linux and macOS
        macls = "/bin/ls"
        if os.path.isfile(macls):
            self.assertEqual(burger.make_exe_path(macls), macls)
            ran_test = True

        # This has to come back false
        selffile = os.path.abspath(__file__)
        self.assertIsNone(burger.make_exe_path(os.path.dirname(selffile)))

        # If this asserts, an executable test wasn't performed
        self.assertTrue(ran_test)

########################################

    def test_import_py_script(self):
        """
        Test burger.import_py_script()
        """

        selffile = os.path.dirname(os.path.abspath(__file__))

        # Load in from the "a" folder
        sample = burger.import_py_script(
            os.path.join(selffile, "data", "sample.py"))
        self.assertEqual(sample.__name__, "sample")
        self.assertTrue(hasattr(sample, "test"))
        self.assertTrue(hasattr(sample, "testa"))
        self.assertFalse(hasattr(sample, "testb"))
        self.assertEqual(sample.test(), "sample_a")
        self.assertEqual(sample.testa(), "testa")

        # Switch to the file in the "b" folder
        sample = burger.import_py_script(
            os.path.join(selffile, "data2", "sample.py"))
        self.assertEqual(sample.__name__, "sample")
        self.assertTrue(hasattr(sample, "test"))
        self.assertFalse(hasattr(sample, "testa"))
        self.assertTrue(hasattr(sample, "testb"))
        self.assertEqual(sample.test(), "sample_b")
        self.assertEqual(sample.testb(), "testb")

        # Test importing a with a unique module name
        sample = burger.import_py_script(
            os.path.join(selffile, "data", "sample.py"), "hamster")
        self.assertEqual(sample.__name__, "hamster")
        self.assertTrue(hasattr(sample, "test"))
        self.assertTrue(hasattr(sample, "testa"))
        self.assertFalse(hasattr(sample, "testb"))
        self.assertEqual(sample.test(), "sample_a")
        self.assertEqual(sample.testa(), "testa")

        self.assertFalse(
            os.path.isfile(
                os.path.join(
                    selffile,
                    "data",
                    "sample.pyc")))
        self.assertFalse(
            os.path.isdir(
                os.path.join(
                    selffile,
                    "data",
                    "__pycache__")))
        self.assertFalse(
            os.path.isfile(
                os.path.join(
                    selffile,
                    "data2",
                    "sample.pyc")))
        self.assertFalse(
            os.path.isdir(
                os.path.join(
                    selffile,
                    "data2",
                    "__pycache__")))

        # Intentionally fail to test the assert that fired
        sample = burger.import_py_script(
            os.path.join(selffile, "doesntexist.py"))
        # File not found is the correct error
        self.assertIsNone(sample)

########################################

    def test_run_py_script(self):
        """
        Test burger.run_py_script()
        """

        selffile = os.path.dirname(os.path.abspath(__file__))
        self.assertEqual(burger.run_py_script(
            os.path.join(selffile, "data", "sample.py"), "test"), "sample_a")
        self.assertEqual(burger.run_py_script(
            os.path.join(selffile, "data", "sample.py"), "testa"), "testa")

        self.assertEqual(burger.run_py_script(
            os.path.join(selffile, "data2", "sample.py"), "test"), "sample_b")
        self.assertEqual(burger.run_py_script(
            os.path.join(selffile, "data2", "sample.py"), "testb"), "testb")

        self.assertEqual(burger.run_py_script(
            os.path.join(
                selffile,
                "data",
                "sample.py"),
            "main",
            "gerbil"), "gerbil")
        self.assertEqual(burger.run_py_script(
            os.path.join(
                selffile,
                "data2",
                "sample.py"),
            "main",
            "cat"), "cattest")

########################################


if __name__ == "__main__":
    unittest.main()
