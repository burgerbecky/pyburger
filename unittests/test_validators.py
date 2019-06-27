#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for burger validator functions

Copyright 2013-2019 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

import burger

# Too few public methods
# pylint: disable=R0903

# Note: (object) is required for python 2.7 compatiblity
# pylint: disable=useless-object-inheritance

########################################


def test_booleanproperty():
    """
    Test burger.BooleanProperty()
    """

    class TestClass(object):
        """ Test """
        test_a = burger.BooleanProperty()
        test_b = burger.BooleanProperty(True)
        test_c = burger.BooleanProperty(False)
        test_d = burger.BooleanProperty(1)

    tester = TestClass()

    # Must return False
    assert tester.test_a is None
    assert tester.test_b is True
    assert tester.test_c is False
    assert tester.test_d is True

    # Write values, ensure they are correct
    tests = (
        ('1', True),
        ('99', True),
        (1, True),
        (0, False),
        (0.0, False),
        (-0.0, False),
        ('-0.0', False),
        ('yes', True),
        ('True', True),
        (True, True),
        (False, False),
        (None, None)
    )
    for test in tests:
        tester.test_b = test[0]
        assert tester.test_b is test[1]

    bad_tests = (
        'skldjsk',
        tester,
        '12s'
    )

    for test in bad_tests:
        try:
            # This MUST throw an exception
            tester.test_b = test
            assert False
        except ValueError:
            pass

    del tester.test_b
    assert tester.test_b is None
