#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for burger string functions

Copyright 2013-2022 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

# pylint: disable=wrong-import-position
# pylint: disable=redundant-u-string-prefix

import sys
import unittest
import os

# Insert the location of burger at the begining so it's the first
# to be processed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import burger

# Needed to help perform Python 2.0 exclusive tests
_PY2 = sys.version_info[0] == 2

########################################


class TestStrings(unittest.TestCase):
    """
    Test the file functions
    """

########################################

    def test_isstring(self):
        """
        Test burger.is_string()
        """

        # unicode not defines
        # flake8: noqa=F821
        # pyright: reportUndefinedVariable=false

        # Must return False
        self.assertFalse(burger.is_string(0))
        self.assertFalse(burger.is_string(None))
        self.assertFalse(burger.is_string(True))
        self.assertFalse(burger.is_string(False))
        self.assertFalse(burger.is_string(1.0))
        self.assertFalse(burger.is_string(()))
        self.assertFalse(burger.is_string({}))
        self.assertFalse(burger.is_string([]))
        self.assertFalse(burger.is_string(bytearray()))
        self.assertFalse(burger.is_string(bytearray(b"abc")))

        # Actual strings
        self.assertTrue(burger.is_string(""))
        self.assertTrue(burger.is_string("a"))
        self.assertTrue(burger.is_string(u"a"))
        self.assertTrue(burger.is_string(b"a"))
        self.assertTrue(burger.is_string(str("a")))
        self.assertTrue(burger.is_string("abc"))
        self.assertTrue(burger.is_string(u"abc"))
        self.assertTrue(burger.is_string(b"abc"))
        self.assertTrue(burger.is_string(str("abc")))

        # Python 2.x tests (Not supported on 3.x or higher)
        if _PY2:
            # pylint: disable=E0602
            self.assertTrue(burger.is_string(unicode("")))
            self.assertTrue(burger.is_string(unicode("a")))
            self.assertTrue(burger.is_string(unicode(u"a")))
            self.assertTrue(burger.is_string(unicode(b"a")))
            self.assertTrue(burger.is_string(unicode("abc")))
            self.assertTrue(burger.is_string(unicode(u"abc")))
            self.assertTrue(burger.is_string(unicode(b"abc")))

        # Bytes need specific encoding passed in for Python 3.0 or higher
        if _PY2:
            self.assertTrue(burger.is_string(bytes("")))
            self.assertTrue(burger.is_string(bytes("a")))
            self.assertTrue(burger.is_string(bytes(u"a")))
        else:
            self.assertTrue(burger.is_string(bytes("", "ascii")))
            self.assertTrue(burger.is_string(bytes("a", "ascii")))
            self.assertTrue(burger.is_string(bytes(u"a", "utf-8")))
        self.assertTrue(burger.is_string(bytes(b"a")))

        if _PY2:
            self.assertTrue(burger.is_string(bytes("abc")))
            self.assertTrue(burger.is_string(bytes(u"abc")))
        else:
            self.assertTrue(burger.is_string(bytes("abc", "ascii")))
            self.assertTrue(burger.is_string(bytes(u"abc", "utf-8")))
        self.assertTrue(burger.is_string(bytes(b"abc")))

        # False if it's a group of strings
        self.assertFalse(burger.is_string(("a",)))
        self.assertFalse(burger.is_string(["a"]))
        self.assertFalse(burger.is_string({"a"}))
        self.assertFalse(burger.is_string(("a", "b")))
        self.assertFalse(burger.is_string(["a", "b"]))
        self.assertFalse(burger.is_string({"a", "b"}))


########################################

    def test_convert_to_array(self):
        """
        Test burger.convert_to_array()
        """

        self.assertEqual(burger.convert_to_array(0), 0)
        self.assertEqual(burger.convert_to_array(None), [])
        self.assertTrue(burger.convert_to_array(True))
        self.assertFalse(burger.convert_to_array(False))
        self.assertEqual(burger.convert_to_array(1.0), 1.0)
        self.assertEqual(burger.convert_to_array(()), ())
        self.assertEqual(burger.convert_to_array({}), {})
        self.assertEqual(burger.convert_to_array([]), [])
        self.assertEqual(burger.convert_to_array(bytearray()), bytearray())
        self.assertEqual(
            burger.convert_to_array(
                bytearray(b"abc")),
            bytearray(b"abc"))

        # Python 2.x tests (Not supported on 3.x or higher)
        if _PY2:
            # pylint: disable=E0602
            self.assertEqual(burger.convert_to_array(unicode("a")), ["a"])
            self.assertEqual(burger.convert_to_array(unicode(u"a")), ["a"])
            self.assertEqual(burger.convert_to_array(unicode(b"a")), ["a"])
            self.assertEqual(burger.convert_to_array(unicode("abc")), ["abc"])
            self.assertEqual(burger.convert_to_array(unicode(u"abc")), ["abc"])
            self.assertEqual(burger.convert_to_array(unicode(b"abc")), ["abc"])

        # Bytes need specific encoding passed in for Python 3.0 or higher
        if _PY2:
            self.assertEqual(burger.convert_to_array(bytes("a")), ["a"])
            self.assertEqual(burger.convert_to_array(bytes(u"a")), ["a"])
        else:
            self.assertEqual(
                burger.convert_to_array(
                    bytes(
                        "a",
                        "ascii")),
                [b"a"])
            self.assertEqual(
                burger.convert_to_array(
                    bytes(
                        u"a",
                        "utf-8")),
                [b"a"])
        self.assertEqual(burger.convert_to_array(bytes(b"a")), [b"a"])

        if _PY2:
            self.assertEqual(burger.convert_to_array(bytes("abc")), [b"abc"])
            self.assertEqual(burger.convert_to_array(bytes(u"abc")), [b"abc"])
        else:
            self.assertEqual(
                burger.convert_to_array(
                    bytes(
                        "abc",
                        "ascii")),
                [b"abc"])
            self.assertEqual(
                burger.convert_to_array(
                    bytes(
                        u"abc",
                        "utf-8")),
                [b"abc"])
        self.assertEqual(burger.convert_to_array(bytes(b"abc")), [b"abc"])

        # False if it's a group of strings
        self.assertEqual(burger.convert_to_array(("a",)), ("a",))
        self.assertEqual(burger.convert_to_array(["a"]), ["a"])
        self.assertEqual(burger.convert_to_array({"a"}), {"a"})
        self.assertEqual(burger.convert_to_array(("a", "b")), ("a", "b"))
        self.assertEqual(burger.convert_to_array(["a", "b"]), ["a", "b"])
        self.assertEqual(burger.convert_to_array({"a", "b"}), {"a", "b"})

########################################

    def test_string_to_bool(self):            # pylint: disable=C0103
        """
        Test burger.string_to_bool()
        """

        true_table = (
            "yes",
            "y",
            "1",
            1,
            1.0,
            True,
            "on",
            "TrUe",
            "t",
            "99",
            99)
        for item in true_table:
            self.assertTrue(burger.string_to_bool(item))

        false_table = ("no", "n", "0", 0, -0.0, False, "off", "FalSe", "f")
        for item in false_table:
            self.assertFalse(burger.string_to_bool(item))

########################################

    def test_TrueFalse(self):            # pylint: disable=C0103
        """
        Test burger.TrueFalse()
        """

        self.assertEqual(burger.TrueFalse(0), "False")
        self.assertEqual(burger.TrueFalse(0.0), "False")
        self.assertEqual(burger.TrueFalse("0"), "False")
        self.assertEqual(burger.TrueFalse("FALSE"), "False")
        self.assertEqual(burger.TrueFalse("false"), "False")
        self.assertEqual(burger.TrueFalse("False"), "False")
        self.assertEqual(burger.TrueFalse(False), "False")
        self.assertEqual(burger.TrueFalse([]), "False")
        self.assertEqual(burger.TrueFalse({}), "False")
        self.assertEqual(burger.TrueFalse(()), "False")

        self.assertEqual(burger.TrueFalse(1), "True")
        self.assertEqual(burger.TrueFalse(1.0), "True")
        self.assertEqual(burger.TrueFalse("1"), "True")
        self.assertEqual(burger.TrueFalse("TRUE"), "True")
        self.assertEqual(burger.TrueFalse("true"), "True")
        self.assertEqual(burger.TrueFalse("True"), "True")
        self.assertEqual(burger.TrueFalse(True), "True")
        self.assertEqual(burger.TrueFalse([1]), "True")
        self.assertEqual(burger.TrueFalse({1}), "True")
        self.assertEqual(burger.TrueFalse((1,)), "True")

        self.assertEqual(burger.TrueFalse("testing"), "True")

########################################

    def test_truefalse(self):
        """
        Test burger.truefalse()
        """

        self.assertEqual(burger.truefalse(0), "false")
        self.assertEqual(burger.truefalse(0.0), "false")
        self.assertEqual(burger.truefalse("0"), "false")
        self.assertEqual(burger.truefalse("FALSE"), "false")
        self.assertEqual(burger.truefalse("false"), "false")
        self.assertEqual(burger.truefalse("False"), "false")
        self.assertEqual(burger.truefalse(False), "false")
        self.assertEqual(burger.truefalse([]), "false")
        self.assertEqual(burger.truefalse({}), "false")
        self.assertEqual(burger.truefalse(()), "false")

        self.assertEqual(burger.truefalse(1), "true")
        self.assertEqual(burger.truefalse(1.0), "true")
        self.assertEqual(burger.truefalse("1"), "true")
        self.assertEqual(burger.truefalse("TRUE"), "true")
        self.assertEqual(burger.truefalse("true"), "true")
        self.assertEqual(burger.truefalse("True"), "true")
        self.assertEqual(burger.truefalse(True), "true")
        self.assertEqual(burger.truefalse([1]), "true")
        self.assertEqual(burger.truefalse({1}), "true")
        self.assertEqual(burger.truefalse((1,)), "true")

        self.assertEqual(burger.truefalse("testing"), "true")

########################################

    def test_TRUEFALSE(self):        # pylint: disable=C0103
        """
        Test burger.TRUEFALSE()
        """

        self.assertEqual(burger.TRUEFALSE(0), "FALSE")
        self.assertEqual(burger.TRUEFALSE(0.0), "FALSE")
        self.assertEqual(burger.TRUEFALSE("0"), "FALSE")
        self.assertEqual(burger.TRUEFALSE("FALSE"), "FALSE")
        self.assertEqual(burger.TRUEFALSE("false"), "FALSE")
        self.assertEqual(burger.TRUEFALSE("False"), "FALSE")
        self.assertEqual(burger.TRUEFALSE(False), "FALSE")
        self.assertEqual(burger.TRUEFALSE([]), "FALSE")
        self.assertEqual(burger.TRUEFALSE({}), "FALSE")
        self.assertEqual(burger.TRUEFALSE(()), "FALSE")

        self.assertEqual(burger.TRUEFALSE(1), "TRUE")
        self.assertEqual(burger.TRUEFALSE(1.0), "TRUE")
        self.assertEqual(burger.TRUEFALSE("1"), "TRUE")
        self.assertEqual(burger.TRUEFALSE("TRUE"), "TRUE")
        self.assertEqual(burger.TRUEFALSE("true"), "TRUE")
        self.assertEqual(burger.TRUEFALSE("True"), "TRUE")
        self.assertEqual(burger.TRUEFALSE(True), "TRUE")
        self.assertEqual(burger.TRUEFALSE([1]), "TRUE")
        self.assertEqual(burger.TRUEFALSE({1}), "TRUE")
        self.assertEqual(burger.TRUEFALSE((1,)), "TRUE")

        self.assertEqual(burger.TRUEFALSE("testing"), "TRUE")

########################################

    def test_convert_to_windows_slashes(self):
        """
        Test burger.convert_to_windows_slashes()
        """

        self.assertEqual(burger.convert_to_windows_slashes(
            "foo", force_ending_slash=False), "foo")
        self.assertEqual(burger.convert_to_windows_slashes(
            "C:/foo\\bar", force_ending_slash=False), "C:\\foo\\bar")
        self.assertEqual(burger.convert_to_windows_slashes(
            "./foo/bar/fug", force_ending_slash=False), ".\\foo\\bar\\fug")
        self.assertEqual(burger.convert_to_windows_slashes(
            ".\\foo\\bar\\fug", force_ending_slash=False), ".\\foo\\bar\\fug")
        self.assertEqual(burger.convert_to_windows_slashes(
            "foo\\", force_ending_slash=False), "foo\\")

        self.assertEqual(burger.convert_to_windows_slashes(
            "foo", force_ending_slash=True), "foo\\")
        self.assertEqual(burger.convert_to_windows_slashes(
            "C:/foo\\bar", force_ending_slash=True), "C:\\foo\\bar\\")
        self.assertEqual(burger.convert_to_windows_slashes(
            "./foo/bar/fug", force_ending_slash=True), ".\\foo\\bar\\fug\\")
        self.assertEqual(burger.convert_to_windows_slashes(
            ".\\foo\\bar\\fug", force_ending_slash=True), ".\\foo\\bar\\fug\\")
        self.assertEqual(burger.convert_to_windows_slashes(
            "foo\\", force_ending_slash=True), "foo\\")

########################################

    def test_convert_to_linux_slashes(self):
        """
        Test burger.convert_to_linux_slashes()
        """

        self.assertEqual(burger.convert_to_linux_slashes(
            "foo", force_ending_slash=False), "foo")
        self.assertEqual(burger.convert_to_linux_slashes(
            "C:/foo\\bar", force_ending_slash=False), "C:/foo/bar")
        self.assertEqual(burger.convert_to_linux_slashes(
            "./foo/bar/fug", force_ending_slash=False), "./foo/bar/fug")
        self.assertEqual(burger.convert_to_linux_slashes(
            ".\\foo\\bar\\fug", force_ending_slash=False), "./foo/bar/fug")
        self.assertEqual(burger.convert_to_linux_slashes(
            "foo\\", force_ending_slash=False), "foo/")

        self.assertEqual(burger.convert_to_linux_slashes(
            "foo", force_ending_slash=True), "foo/")
        self.assertEqual(burger.convert_to_linux_slashes(
            "C:/foo\\bar", force_ending_slash=True), "C:/foo/bar/")
        self.assertEqual(burger.convert_to_linux_slashes(
            "./foo/bar/fug", force_ending_slash=True), "./foo/bar/fug/")
        self.assertEqual(burger.convert_to_linux_slashes(
            ".\\foo\\bar\\fug",
            force_ending_slash=True), "./foo/bar/fug/")
        self.assertEqual(burger.convert_to_linux_slashes(
            "foo\\", force_ending_slash=True), "foo/")

########################################

    def test_encapsulate_path_windows(self):
        """
        Test burger.encapsulate_path_windows()
        """

        self.assertEqual(burger.encapsulate_path_windows(""), "\"\"")
        self.assertEqual(burger.encapsulate_path_windows("foo"), "foo")
        self.assertEqual(burger.encapsulate_path_windows("f$oo"), "\"f$oo\"")
        self.assertEqual(burger.encapsulate_path_windows(
            "f\"oo"), "\"f\\\"oo\"")
        self.assertEqual(
            burger.encapsulate_path_windows("foo'foo"),
            "\"foo'foo\"")

########################################

    def test_encapsulate_path_linux(self):
        """
        Test burger.encapsulate_path_linux()
        """

        self.assertEqual(burger.encapsulate_path_linux(""), "''")
        self.assertEqual(burger.encapsulate_path_linux("foo"), "foo")
        self.assertEqual(burger.encapsulate_path_linux("f$oo"), "'f$oo'")
        self.assertEqual(burger.encapsulate_path_linux("f\"oo"), "'f\"oo'")
        self.assertEqual(
            burger.encapsulate_path_linux("foo'foo"),
            "'foo'\"'\"'foo'")

########################################

    def test_encapsulate_path(self):
        """
        Test burger.encapsulate_path()
        """

        savedname = burger.strutils.IS_WINDOWS
        # Hack to force windows mode
        burger.strutils.IS_WINDOWS = True
        self.assertEqual(burger.encapsulate_path(""), "\"\"")
        self.assertEqual(burger.encapsulate_path("foo"), "foo")
        self.assertEqual(burger.encapsulate_path("f$oo"), "\"f$oo\"")
        self.assertEqual(burger.encapsulate_path("f\"oo"), "\"f\\\"oo\"")
        self.assertEqual(burger.encapsulate_path("foo'foo"), "\"foo'foo\"")

        # Hack to force linux mode
        burger.strutils.IS_WINDOWS = False
        self.assertEqual(burger.encapsulate_path(""), "''")
        self.assertEqual(burger.encapsulate_path("foo"), "foo")
        self.assertEqual(burger.encapsulate_path("f$oo"), "'f$oo'")
        self.assertEqual(burger.encapsulate_path("f\"oo"), "'f\"oo'")
        self.assertEqual(burger.encapsulate_path("foo'foo"), "'foo'\"'\"'foo'")
        # Restore the real value
        burger.strutils.IS_WINDOWS = savedname

########################################

    def test_split_comma_with_quotes(self):
        """
        Test burger.split_comma_with_quotes()
        """

        # Test for normal behavior
        self.assertEqual(burger.split_comma_with_quotes("x"), ["x"])
        self.assertEqual(burger.split_comma_with_quotes("x,y"), ["x", "y"])
        self.assertEqual(burger.split_comma_with_quotes("x,y,"), ["x", "y"])
        self.assertEqual(
            burger.split_comma_with_quotes("x,y,z,"), [
                "x", "y", "z"])
        self.assertEqual(
            burger.split_comma_with_quotes(",x,y,z"), [
                "", "x", "y", "z"])
        self.assertEqual(
            burger.split_comma_with_quotes(",x,y,z,"), [
                "", "x", "y", "z"])

        # Test for normal behavior
        self.assertEqual(burger.split_comma_with_quotes("\nx"), ["\nx"])
        self.assertEqual(burger.split_comma_with_quotes("\tx,y"), ["\tx", "y"])
        self.assertEqual(burger.split_comma_with_quotes(
            "\rx,y,"), ["\rx", "y"])
        self.assertEqual(burger.split_comma_with_quotes("\n\rx,y,z,"), [
            "\n\rx", "y", "z"])
        self.assertEqual(burger.split_comma_with_quotes(
            ",x,y,z\t"), ["", "x", "y", "z\t"])
        self.assertEqual(burger.split_comma_with_quotes(
            ",x,y,z\t,"), ["", "x", "y", "z\t"])

        # Test for quote behavior
        self.assertEqual(burger.split_comma_with_quotes("\"x\""), ["\"x\""])
        self.assertEqual(
            burger.split_comma_with_quotes("\"x\",\"y\""), [
                "\"x\"", "\"y\""])
        self.assertEqual(burger.split_comma_with_quotes(
            "\"x\",y,"), ["\"x\"", "y"])
        self.assertEqual(
            burger.split_comma_with_quotes("x,'y',z,"), [
                "x", "'y'", "z"])
        self.assertEqual(burger.split_comma_with_quotes(
            ",x,y,\"z\""), ["", "x", "y", "\"z\""])
        self.assertEqual(
            burger.split_comma_with_quotes(",x,\"y,z\","), [
                "", "x", "\"y,z\""])

        # Test for Exceptions
        self.assertRaises(ValueError, burger.split_comma_with_quotes, "'foo")

        self.assertRaises(ValueError, burger.split_comma_with_quotes, "\"foo")

        self.assertRaises(
            ValueError,
            burger.split_comma_with_quotes,
            "\"foo,bar")


########################################


    def test_parse_csv(self):
        """
        Test burger.parse_csv()
        """

        # Test for normal behavior
        self.assertEqual(burger.parse_csv("x"), ["x"])
        self.assertEqual(burger.parse_csv("x,y"), ["x", "y"])
        self.assertEqual(burger.parse_csv("x,y,"), ["x", "y"])
        self.assertEqual(burger.parse_csv("x,y,z,"), ["x", "y", "z"])
        self.assertEqual(burger.parse_csv(",x,y,z"), ["", "x", "y", "z"])
        self.assertEqual(burger.parse_csv(",x,y,z,"), ["", "x", "y", "z"])

        # Test for normal behavior
        self.assertEqual(burger.parse_csv("\nx"), ["x"])
        self.assertEqual(burger.parse_csv("\tx,y"), ["x", "y"])
        self.assertEqual(burger.parse_csv("\rx,y,"), ["x", "y"])
        self.assertEqual(burger.parse_csv("\n\rx,y,z,"), ["x", "y", "z"])
        self.assertEqual(burger.parse_csv(",x,y,z\t"), ["", "x", "y", "z"])
        self.assertEqual(burger.parse_csv(",x,y,z\t,"), ["", "x", "y", "z"])

        # Test for quote behavior
        self.assertEqual(burger.parse_csv("\"x\""), ["x"])
        self.assertEqual(burger.parse_csv("\"x\",\"y\""), ["x", "y"])
        self.assertEqual(burger.parse_csv("\"x\",y,"), ["x", "y"])
        self.assertEqual(burger.parse_csv("x,\"y\",z,"), ["x", "y", "z"])
        self.assertEqual(burger.parse_csv(",x,y,\"z\""), ["", "x", "y", "z"])
        self.assertEqual(burger.parse_csv(",x,\"y,z\","), ["", "x", "y,z"])
        self.assertEqual(burger.parse_csv("x,\"y\"\"z\","), ["x", "y\"z"])
        self.assertEqual(burger.parse_csv("x,'y''z',"), ["x", "y'z"])

        # Test for Exceptions
        self.assertRaises(ValueError, burger.parse_csv, "'foo")
        self.assertRaises(ValueError, burger.parse_csv, "\"foo")
        self.assertRaises(ValueError, burger.parse_csv, "\"foo,bar")

########################################

    def test_translate_to_regex_match(self):
        """
        Test burger.translate_to_regex_match()
        """

        # Get an empty list
        self.assertFalse(burger.translate_to_regex_match([]))

        dir_list = burger.translate_to_regex_match(("foo.txt", "*.py"))
        self.assertTrue(dir_list)

        # Find positive matches
        for item in dir_list:
            self.assertTrue(item("foo.txt") or item("a.py"))
            self.assertFalse(item("foo.bar"))
            self.assertFalse(item("py.px"))
            self.assertFalse(item("py"))


########################################


    def test_escape_xml_cdata(self):
        """
        Test burger.escape_xml_cdata()
        """

        tests = (
            ("before", "before"),
            ("foo&foo", "foo&amp;foo"),
            ("<token>", "&lt;token&gt;"),
            ("\"quotes\"\n", "\"quotes\"\n")
        )

        for test in tests:
            self.assertEqual(burger.escape_xml_cdata(test[0]), test[1])


########################################


    def test_escape_xml_attribute(self):
        """
        Test burger.escape_xml_attribute()
        """

        tests = (
            ("before", "before"),
            ("foo&foo", "foo&amp;foo"),
            ("<token>", "&lt;token&gt;"),
            ("\"quotes\"\n", "&quot;quotes&quot;&#10;"),
            ("\r\n\n\r", "&#10;&#10;&#10;"),
            ("mac\rstring", "mac&#10;string"),
            ("linux\nstring", "linux&#10;string"),
            ("pc\r\nstring", "pc&#10;string"),
            ("test\ttabs\tnow", "test&#09;tabs&#09;now")
        )

        for test in tests:
            self.assertEqual(burger.escape_xml_attribute(test[0]), test[1])

########################################

    def test_packed_paths(self):
        """
        Test burger.packed_paths()
        """

        tests = (
            ("test", "test"),
            (("foo", "bar"), "foo;bar"),
            (["a", "b", "c"], "a;b;c"),
            (["a", "bart", "c/c"], "a;bart;c/c")
        )

        for test in tests:
            self.assertEqual(burger.packed_paths(test[0]), test[1])

        # Test separator replacement
        separators = (
            ("a", ";", ":", "\n")
        )

        for sep in separators:
            for test in tests:
                self.assertEqual(burger.packed_paths(
                    test[0],
                    separator=sep), test[1].replace(
                        ";", sep))

        # Test slashes and forced ending
        paths = (
            "c:\\foo\\bar",
            "/home/usr/bar",
            "~/.config",
            "foobar.txt",
            "c:\\foo\\bar\\",
            "/home/usr/bar/",
            "~/.config/",
            "/break\\me",
            "\\fun\\fun\\"
        )

        for path in paths:
            self.assertEqual(burger.packed_paths(
                path, slashes="/"), path.replace("\\", "/"))
            self.assertEqual(burger.packed_paths(
                path, slashes="\\"), path.replace(
                    "/", "\\"))

            temp = path.replace("\\", "/")
            if not temp.endswith("/"):
                temp = temp + "/"
            self.assertEqual(burger.packed_paths(
                path, slashes="/", force_ending_slash=True), temp)

            temp = path.replace("/", "\\")
            if not temp.endswith("\\"):
                temp = temp + "\\"
            self.assertEqual(burger.packed_paths(
                path, slashes="\\", force_ending_slash=True), temp)

########################################

    def test_make_version_tuple(self):
        """
        Test burger.make_version_tuple()
        """

        self.assertEqual(burger.make_version_tuple("0.0.0"), (0, 0, 0))
        self.assertEqual(burger.make_version_tuple("12.34.56"), (12, 34, 56))
        self.assertEqual(burger.make_version_tuple("1.0.1.2rc"), (1, 0, 1, 2))
        self.assertEqual(burger.make_version_tuple("1.2.9.beta"), (1, 2, 9))
        self.assertEqual(burger.make_version_tuple("1.2.beta.9"), (1, 2))
        self.assertEqual(burger.make_version_tuple("4"), (4,))
        self.assertEqual(burger.make_version_tuple("1,2,3"), (1,))
        self.assertEqual(burger.make_version_tuple("foobar"), tuple())
        self.assertEqual(burger.make_version_tuple(
            "1.2.3.4.5.6.7"), (1, 2, 3, 4, 5, 6, 7))
        self.assertEqual(burger.make_version_tuple(None), tuple())
        self.assertEqual(burger.make_version_tuple(""), tuple())
        self.assertEqual(burger.make_version_tuple(1.0), tuple())
        self.assertEqual(burger.make_version_tuple([]), tuple())
        self.assertEqual(burger.make_version_tuple(()), tuple())
        self.assertEqual(burger.make_version_tuple({}), tuple())
        self.assertEqual(burger.make_version_tuple(burger), tuple())

########################################


if __name__ == "__main__":
    unittest.main()
