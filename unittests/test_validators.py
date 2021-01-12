#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for burger validator functions

Copyright 2013-2021 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

# pylint: disable=wrong-import-position

import sys
import unittest
import os

# Insert the location of burger at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import burger

# Too few public methods
# pylint: disable=R0903

# Note: (object) is required for python 2.7 compatiblity
# pylint: disable=useless-object-inheritance

########################################


class TestValidators(unittest.TestCase):
    """
    Test the file functions
    """

########################################

    def test_booleanproperty(self):
        """
        Test burger.BooleanProperty()
        """

        class TestClass(object):
            """ Test """
            test_a = burger.BooleanProperty('_test_a')
            test_b = burger.BooleanProperty('_test_b')
            test_c = burger.BooleanProperty('_test_c')
            test_d = burger.BooleanProperty('_test_d')

            def __init__(self):
                self.test_b = True
                self.test_c = False
                self.test_d = 1

        tester = TestClass()

        # Must return False
        self.assertIsNone(tester.test_a)
        self.assertTrue(tester.test_b)
        self.assertFalse(tester.test_c)
        self.assertTrue(tester.test_d)

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
            self.assertIs(tester.test_b, test[1])

        bad_tests = (
            'skldjsk',
            tester,
            '12s'
        )

        for test in bad_tests:
            # This MUST throw an exception
            with self.assertRaises(ValueError):
                tester.test_b = test

        # Test for unique values across class instances
        bester = TestClass()
        tester.test_a = True
        bester.test_a = False

        self.assertTrue(tester.test_a)
        self.assertFalse(bester.test_a)

########################################

    def test_integerproperty(self):
        """
        Test burger.IntegerProperty()
        """

        class TestClass(object):
            """ Test """
            test_a = burger.IntegerProperty('_test_a')
            test_b = burger.IntegerProperty('_test_b')
            test_c = burger.IntegerProperty('_test_c')
            test_d = burger.IntegerProperty('_test_d')

            def __init__(self):
                self.test_b = True
                self.test_c = False
                self.test_d = 1

        tester = TestClass()

        # Must return False
        self.assertIsNone(tester.test_a)
        self.assertEqual(tester.test_b, 1)
        self.assertEqual(tester.test_c, 0)
        self.assertEqual(tester.test_d, 1)

        # Write values, ensure they are correct
        tests = (
            ('1', 1),
            ('99', 99),
            (1, 1),
            (0, 0),
            (0.0, 0),
            (-0.0, 0),
            ('-0.0', 0),
            (0x7FFFFFFFFFFFFFFF, 0x7FFFFFFFFFFFFFFF),
            (-0x8000000000000000, -0x8000000000000000),
            ('0x7FFFFFFFFFFFFFFF', 0x7FFFFFFFFFFFFFFF),
            ('-0x8000000000000000', -0x8000000000000000),
            (True, 1),
            (False, 0),
            (None, None)
        )
        for test in tests:
            tester.test_b = test[0]
            self.assertEqual(tester.test_b, test[1])

        bad_tests = (
            'skldjsk',
            tester,
            '12s',
            '0xFFFFFFFFFFFFFFFFF',
            '1.e+20',
            'NaN'
        )

        for test in bad_tests:
            # This MUST throw an exception
            with self.assertRaises(ValueError):
                tester.test_b = test
                if tester.test_b != tester.test_b:
                    pass

        # Test for unique values across class instances
        bester = TestClass()
        tester.test_a = 1
        bester.test_a = 2

        self.assertEqual(tester.test_a, 1)
        self.assertEqual(bester.test_a, 2)


########################################

    def test_stringproperty(self):
        """
        Test burger.StringProperty()
        """

        class TestClass(object):
            """ Test """
            test_a = burger.StringProperty('_test_a')
            test_b = burger.StringProperty('_test_b')
            test_c = burger.StringProperty('_test_c')
            test_d = burger.StringProperty('_test_d')

            def __init__(self):
                self.test_b = True
                self.test_c = 'True'
                self.test_d = 1

        tester = TestClass()

        # Must return False
        self.assertIsNone(tester.test_a)
        self.assertEqual(tester.test_b, 'True')
        self.assertEqual(tester.test_c, 'True')
        self.assertEqual(tester.test_d, '1')

        # Write values, ensure they are correct
        tests = (
            ('1', '1'),
            ('99', '99'),
            (1, '1'),
            (0, '0'),
            (0.0, '0.0'),
            (-0.0, '-0.0'),
            ('-0.0', '-0.0'),
            ('yes', 'yes'),
            ('True', 'True'),
            (True, 'True'),
            (False, 'False'),
            ([1, 2, 3], '[1, 2, 3]'),
            ((1, 2, 3), '(1, 2, 3)'),
            (None, None)
        )
        for test in tests:
            tester.test_b = test[0]
            self.assertEqual(tester.test_b, test[1])

        # Test for unique values across class instances
        bester = TestClass()
        tester.test_a = 'foo'
        bester.test_a = 'bar'

        self.assertEqual(tester.test_a, 'foo')
        self.assertEqual(bester.test_a, 'bar')

########################################

    def test_stringlistproperty(self):
        """
        Test burger.StringListProperty()
        """

        class TestClass(object):
            """ Test """
            test_a = burger.StringListProperty('_test_a')
            test_b = burger.StringListProperty('_test_b')
            test_c = burger.StringListProperty('_test_c')
            test_d = burger.StringListProperty('_test_d')

            def __init__(self):
                self.test_b = True
                self.test_c = 'True'
                self.test_d = ['a', 'b', 'c']

        tester = TestClass()

        # Must return False
        self.assertEqual(tester.test_a, [])
        self.assertEqual(tester.test_b, ['True'])
        self.assertEqual(tester.test_c, ['True'])
        self.assertEqual(tester.test_d, ['a', 'b', 'c'])

        # Write values, ensure they are correct
        tests = (
            ('1', ['1']),
            ('99', ['99']),
            (1, ['1']),
            (0, ['0']),
            (0.0, ['0.0']),
            (-0.0, ['-0.0']),
            ('-0.0', ['-0.0']),
            ('yes', ['yes']),
            ('True', ['True']),
            (True, ['True']),
            (False, ['False']),
            ([1, 2, 3], ['1', '2', '3']),
            ((1, 2, 3), ['1', '2', '3']),
            (None, [])
        )
        for test in tests:
            tester.test_b = test[0]
            self.assertEqual(tester.test_b, test[1])

        # Test for unique values across class instances
        bester = TestClass()
        tester.test_a = 'foo'
        bester.test_a = 'bar'

        self.assertEqual(tester.test_a, ['foo'])
        self.assertEqual(bester.test_a, ['bar'])

########################################

    def test_enumproperty(self):
        """
        Test burger.EnumProperty()
        """

        j = (('a', 'b', 'c'), 'd', 'e', ['f', 'g', 'h'], 'i')
        k = (('f', 'g', 'h'), 'e', 'd', ['a', 'b', 'c'], 'i')

        class TestClass(object):
            """ Test """
            test_a = burger.EnumProperty('_test_a', j)
            test_b = burger.EnumProperty('_test_b', j)
            test_c = burger.EnumProperty('_test_c', j)
            test_d = burger.EnumProperty('_test_d', j)
            test_e = burger.EnumProperty('_test_e', k)

            def __init__(self):
                self.test_b = 'i'
                self.test_c = 2
                self.test_d = 'c'
                self.test_e = 'c'

        tester = TestClass()

        # Must return False
        self.assertIsNone(tester.test_a)
        self.assertEqual(tester.test_b, 4)
        self.assertEqual(tester.test_c, 2)
        self.assertEqual(tester.test_d, 0)

        # Write values, ensure they are correct
        tests = (
            ('a', 0),
            ('b', 0),
            ('c', 0),
            (0, 0),
            (0.0, 0),
            (-0.0, 0),
            (3, 3),
            ('d', 1),
            ('e', 2),
            ('f', 3),
            ('g', 3),
            ('h', 3),
            ('i', 4),
            (None, None)
        )
        for test in tests:
            tester.test_b = test[0]
            self.assertEqual(tester.test_b, test[1])

        # Test for unique values across class instances
        bester = TestClass()
        tester.test_a = 'a'
        bester.test_a = 'i'

        self.assertEqual(tester.test_a, 0)
        self.assertEqual(bester.test_a, 4)

        tester.test_a = 'f'
        tester.test_e = 'f'
        self.assertEqual(tester.test_a, 3)
        self.assertEqual(tester.test_e, 0)

        class BestClass(object):
            """ Test """
            test_a = burger.EnumProperty('_test_a', [])

            def __init__(self, enums):
                self._test_a_enums = enums

        tester = BestClass(j)
        bester = BestClass(k)

        tester.test_a = 'f'
        bester.test_a = 'f'
        self.assertEqual(tester.test_a, 3)
        self.assertEqual(bester.test_a, 0)

########################################

    def test_noneproperty(self):
        """
        Test burger.NoneProperty()
        """

        class TestClass(object):
            """ Test """
            test_a = burger.NoneProperty('_test_a')
            test_b = burger.NoneProperty('_test_b')

        tester = TestClass()

        # Must return None
        self.assertIsNone(tester.test_a)
        self.assertIsNone(tester.test_b)

        # Write values, ensure they are correct
        tests = (
            '1',
            '99',
            1,
            0,
            0.0,
            -0.0,
            '-0.0',
            'yes',
            'True',
            True,
            False,
        )

        for test in tests:
           # This MUST throw an exception
            with self.assertRaises(ValueError):
                tester.test_b = test

            self.assertIsNone(tester.test_b)

        bad_tests = (
            'skldjsk',
            tester,
            '12s'
        )

        for test in bad_tests:
           # This MUST throw an exception
            with self.assertRaises(ValueError):
                tester.test_b = test

        # Test for unique values across class instances
        bester = TestClass()
        tester.test_a = None
        bester.test_a = None

        self.assertIsNone(tester.test_a)
        self.assertIsNone(bester.test_a)

########################################


if __name__ == '__main__':
    unittest.main()
