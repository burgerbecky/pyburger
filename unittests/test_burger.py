#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger class functions

Copyright 2021-2024 by Rebecca Ann Heineman becky@burgerbecky.com

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

# Insert the location of burger at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from burger import Interceptstdout

########################################


class TestBurger(unittest.TestCase):
    """
    Test the burger classes
    """

########################################

    def test_interceptstdout(self):
        """
        Test burger.Interceptstdout
        """

        with Interceptstdout() as output:
            print("Kill me")
            print("Line 2")
            print("")

        self.assertEqual(output, ["Kill me", "Line 2", ""])


########################################


if __name__ == "__main__":
    unittest.main()
