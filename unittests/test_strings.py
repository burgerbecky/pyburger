#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for burger string functions

Copyright 2013-2019 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

import sys
import os
import burger

# Needed to help perform Python 2.0 exclusive tests
_PY2 = sys.version_info[0] == 2

########################################


def test_isstring():
    """
    Test burger.is_string()
    """

    # Must return False
    assert not burger.is_string(0)
    assert not burger.is_string(None)
    assert not burger.is_string(True)
    assert not burger.is_string(False)
    assert not burger.is_string(1.0)
    assert not burger.is_string(())
    assert not burger.is_string({})
    assert not burger.is_string([])
    assert not burger.is_string(bytearray())
    assert not burger.is_string(bytearray(b'abc'))

    # Actual strings
    assert burger.is_string('')
    assert burger.is_string('a')
    assert burger.is_string(u'a')
    assert burger.is_string(b'a')
    assert burger.is_string(str('a'))
    assert burger.is_string('abc')
    assert burger.is_string(u'abc')
    assert burger.is_string(b'abc')
    assert burger.is_string(str('abc'))

    # Python 2.x tests (Not supported on 3.x or higher)
    if _PY2:
        # pylint: disable=E0602
        assert burger.is_string(unicode(''))
        assert burger.is_string(unicode('a'))
        assert burger.is_string(unicode(u'a'))
        assert burger.is_string(unicode(b'a'))
        assert burger.is_string(unicode('abc'))
        assert burger.is_string(unicode(u'abc'))
        assert burger.is_string(unicode(b'abc'))

    # Bytes need specific encoding passed in for Python 3.0 or higher
    if _PY2:
        assert burger.is_string(bytes(''))
        assert burger.is_string(bytes('a'))
        assert burger.is_string(bytes(u'a'))
    else:
        assert burger.is_string(bytes('', 'ascii'))
        assert burger.is_string(bytes('a', 'ascii'))
        assert burger.is_string(bytes(u'a', 'utf-8'))
    assert burger.is_string(bytes(b'a'))

    if _PY2:
        assert burger.is_string(bytes('abc'))
        assert burger.is_string(bytes(u'abc'))
    else:
        assert burger.is_string(bytes('abc', 'ascii'))
        assert burger.is_string(bytes(u'abc', 'utf-8'))
    assert burger.is_string(bytes(b'abc'))

    # False if it's a group of strings
    assert not burger.is_string(('a',))
    assert not burger.is_string(['a'])
    assert not burger.is_string({'a'})
    assert not burger.is_string(('a', 'b'))
    assert not burger.is_string(['a', 'b'])
    assert not burger.is_string({'a', 'b'})


########################################


def test_convert_to_array():
    """
    Test burger.convert_to_array()
    """

    assert burger.convert_to_array(0) == 0
    assert burger.convert_to_array(None) == []
    assert burger.convert_to_array(True) is True
    assert burger.convert_to_array(False) is False
    assert burger.convert_to_array(1.0) == 1.0
    assert burger.convert_to_array(()) == ()
    assert burger.convert_to_array({}) == {}
    assert burger.convert_to_array([]) == []
    assert burger.convert_to_array(bytearray()) == bytearray()
    assert burger.convert_to_array(bytearray(b'abc')) == bytearray(b'abc')

    # Python 2.x tests (Not supported on 3.x or higher)
    if _PY2:
        # pylint: disable=E0602
        assert burger.convert_to_array(unicode('a')) == ['a']
        assert burger.convert_to_array(unicode(u'a')) == ['a']
        assert burger.convert_to_array(unicode(b'a')) == ['a']
        assert burger.convert_to_array(unicode('abc')) == ['abc']
        assert burger.convert_to_array(unicode(u'abc')) == ['abc']
        assert burger.convert_to_array(unicode(b'abc')) == ['abc']

    # Bytes need specific encoding passed in for Python 3.0 or higher
    if _PY2:
        assert burger.convert_to_array(bytes('a')) == ['a']
        assert burger.convert_to_array(bytes(u'a')) == ['a']
    else:
        assert burger.convert_to_array(bytes('a', 'ascii')) == [b'a']
        assert burger.convert_to_array(bytes(u'a', 'utf-8')) == [b'a']
    assert burger.convert_to_array(bytes(b'a')) == [b'a']

    if _PY2:
        assert burger.convert_to_array(bytes('abc')) == [b'abc']
        assert burger.convert_to_array(bytes(u'abc')) == [b'abc']
    else:
        assert burger.convert_to_array(bytes('abc', 'ascii')) == [b'abc']
        assert burger.convert_to_array(bytes(u'abc', 'utf-8')) == [b'abc']
    assert burger.convert_to_array(bytes(b'abc')) == [b'abc']

    # False if it's a group of strings
    assert burger.convert_to_array(('a',)) == ('a',)
    assert burger.convert_to_array(['a']) == ['a']
    assert burger.convert_to_array({'a'}) == {'a'}
    assert burger.convert_to_array(('a', 'b')) == ('a', 'b')
    assert burger.convert_to_array(['a', 'b']) == ['a', 'b']
    assert burger.convert_to_array({'a', 'b'}) == {'a', 'b'}

########################################


def test_TrueFalse():            # pylint: disable=C0103
    """
    Test burger.TrueFalse()
    """

    assert burger.TrueFalse(0) == 'False'
    assert burger.TrueFalse(0.0) == 'False'
    assert burger.TrueFalse('0') == 'False'
    assert burger.TrueFalse('FALSE') == 'False'
    assert burger.TrueFalse('false') == 'False'
    assert burger.TrueFalse('False') == 'False'
    assert burger.TrueFalse(False) == 'False'
    assert burger.TrueFalse([]) == 'False'
    assert burger.TrueFalse({}) == 'False'
    assert burger.TrueFalse(()) == 'False'

    assert burger.TrueFalse(1) == 'True'
    assert burger.TrueFalse(1.0) == 'True'
    assert burger.TrueFalse('1') == 'True'
    assert burger.TrueFalse('TRUE') == 'True'
    assert burger.TrueFalse('true') == 'True'
    assert burger.TrueFalse('True') == 'True'
    assert burger.TrueFalse(True) == 'True'
    assert burger.TrueFalse([1]) == 'True'
    assert burger.TrueFalse({1}) == 'True'
    assert burger.TrueFalse((1)) == 'True'

    assert burger.TrueFalse('testing') == 'True'

########################################


def test_truefalse():
    """
    Test burger.truefalse()
    """

    assert burger.truefalse(0) == 'false'
    assert burger.truefalse(0.0) == 'false'
    assert burger.truefalse('0') == 'false'
    assert burger.truefalse('FALSE') == 'false'
    assert burger.truefalse('false') == 'false'
    assert burger.truefalse('False') == 'false'
    assert burger.truefalse(False) == 'false'
    assert burger.truefalse([]) == 'false'
    assert burger.truefalse({}) == 'false'
    assert burger.truefalse(()) == 'false'

    assert burger.truefalse(1) == 'true'
    assert burger.truefalse(1.0) == 'true'
    assert burger.truefalse('1') == 'true'
    assert burger.truefalse('TRUE') == 'true'
    assert burger.truefalse('true') == 'true'
    assert burger.truefalse('True') == 'true'
    assert burger.truefalse(True) == 'true'
    assert burger.truefalse([1]) == 'true'
    assert burger.truefalse({1}) == 'true'
    assert burger.truefalse((1)) == 'true'

    assert burger.truefalse('testing') == 'true'

########################################


def test_TRUEFALSE():        # pylint: disable=C0103
    """
    Test burger.TRUEFALSE()
    """

    assert burger.TRUEFALSE(0) == 'FALSE'
    assert burger.TRUEFALSE(0.0) == 'FALSE'
    assert burger.TRUEFALSE('0') == 'FALSE'
    assert burger.TRUEFALSE('FALSE') == 'FALSE'
    assert burger.TRUEFALSE('false') == 'FALSE'
    assert burger.TRUEFALSE('False') == 'FALSE'
    assert burger.TRUEFALSE(False) == 'FALSE'
    assert burger.TRUEFALSE([]) == 'FALSE'
    assert burger.TRUEFALSE({}) == 'FALSE'
    assert burger.TRUEFALSE(()) == 'FALSE'

    assert burger.TRUEFALSE(1) == 'TRUE'
    assert burger.TRUEFALSE(1.0) == 'TRUE'
    assert burger.TRUEFALSE('1') == 'TRUE'
    assert burger.TRUEFALSE('TRUE') == 'TRUE'
    assert burger.TRUEFALSE('true') == 'TRUE'
    assert burger.TRUEFALSE('True') == 'TRUE'
    assert burger.TRUEFALSE(True) == 'TRUE'
    assert burger.TRUEFALSE([1]) == 'TRUE'
    assert burger.TRUEFALSE({1}) == 'TRUE'
    assert burger.TRUEFALSE((1)) == 'TRUE'

    assert burger.TRUEFALSE('testing') == 'TRUE'

########################################


def test_convert_to_windows_slashes():
    """
    Test burger.convert_to_windows_slashes()
    """

    assert burger.convert_to_windows_slashes(
        'foo', force_ending_slash=False) == 'foo'
    assert burger.convert_to_windows_slashes(
        'C:/foo\\bar', force_ending_slash=False) == 'C:\\foo\\bar'
    assert burger.convert_to_windows_slashes(
        './foo/bar/fug', force_ending_slash=False) == '.\\foo\\bar\\fug'
    assert burger.convert_to_windows_slashes(
        '.\\foo\\bar\\fug', force_ending_slash=False) == '.\\foo\\bar\\fug'
    assert burger.convert_to_windows_slashes(
        'foo\\', force_ending_slash=False) == 'foo\\'

    assert burger.convert_to_windows_slashes(
        'foo', force_ending_slash=True) == 'foo\\'
    assert burger.convert_to_windows_slashes(
        'C:/foo\\bar', force_ending_slash=True) == 'C:\\foo\\bar\\'
    assert burger.convert_to_windows_slashes(
        './foo/bar/fug', force_ending_slash=True) == '.\\foo\\bar\\fug\\'
    assert burger.convert_to_windows_slashes(
        '.\\foo\\bar\\fug', force_ending_slash=True) == '.\\foo\\bar\\fug\\'
    assert burger.convert_to_windows_slashes(
        'foo\\', force_ending_slash=True) == 'foo\\'

########################################


def test_convert_to_linux_slashes():
    """
    Test burger.convert_to_linux_slashes()
    """

    assert burger.convert_to_linux_slashes(
        'foo', force_ending_slash=False) == 'foo'
    assert burger.convert_to_linux_slashes(
        'C:/foo\\bar', force_ending_slash=False) == 'C:/foo/bar'
    assert burger.convert_to_linux_slashes(
        './foo/bar/fug', force_ending_slash=False) == './foo/bar/fug'
    assert burger.convert_to_linux_slashes(
        '.\\foo\\bar\\fug', force_ending_slash=False) == './foo/bar/fug'
    assert burger.convert_to_linux_slashes(
        'foo\\', force_ending_slash=False) == 'foo/'

    assert burger.convert_to_linux_slashes(
        'foo', force_ending_slash=True) == 'foo/'
    assert burger.convert_to_linux_slashes('C:/foo\\bar',
                                           force_ending_slash=True) == 'C:/foo/bar/'
    assert burger.convert_to_linux_slashes('./foo/bar/fug',
                                           force_ending_slash=True) == './foo/bar/fug/'
    assert burger.convert_to_linux_slashes('.\\foo\\bar\\fug',
                                           force_ending_slash=True) == './foo/bar/fug/'
    assert burger.convert_to_linux_slashes(
        'foo\\', force_ending_slash=True) == 'foo/'

########################################


def test_encapsulate_path_windows():
    """
    Test burger.encapsulate_path_windows()
    """

    assert burger.encapsulate_path_windows('') == '""'
    assert burger.encapsulate_path_windows('foo') == 'foo'
    assert burger.encapsulate_path_windows('f$oo') == '"f$oo"'
    assert burger.encapsulate_path_windows('f"oo') == '"f\\"oo"'
    assert burger.encapsulate_path_windows("foo'foo") == '"foo\'foo"'

########################################


def test_encapsulate_path_linux():
    """
    Test burger.encapsulate_path_linux()
    """

    assert burger.encapsulate_path_linux('') == "''"
    assert burger.encapsulate_path_linux('foo') == "foo"
    assert burger.encapsulate_path_linux('f$oo') == "'f$oo'"
    assert burger.encapsulate_path_linux('f"oo') == "'f\"oo'"
    assert burger.encapsulate_path_linux("foo'foo") == "'foo'\"'\"'foo'"

########################################


def test_encapsulate_path():
    """
    Test burger.encapsulate_path()
    """

    savedname = os.name
    # Hack to force windows mode
    os.name = 'nt'
    assert burger.encapsulate_path('') == '""'
    assert burger.encapsulate_path('foo') == 'foo'
    assert burger.encapsulate_path('f$oo') == '"f$oo"'
    assert burger.encapsulate_path('f"oo') == '"f\\"oo"'
    assert burger.encapsulate_path("foo'foo") == '"foo\'foo"'

    # Hack to force linux mode
    os.name = 'linux'
    assert burger.encapsulate_path('') == "''"
    assert burger.encapsulate_path('foo') == "foo"
    assert burger.encapsulate_path('f$oo') == "'f$oo'"
    assert burger.encapsulate_path('f"oo') == "'f\"oo'"
    assert burger.encapsulate_path("foo'foo") == "'foo'\"'\"'foo'"
    # Restore the real value
    os.name = savedname

########################################


def test_split_comma_with_quotes():
    """
    Test burger.split_comma_with_quotes()
    """

    # Test for normal behavior
    assert burger.split_comma_with_quotes('x') == ['x']
    assert burger.split_comma_with_quotes('x,y') == ['x', 'y']
    assert burger.split_comma_with_quotes('x,y,') == ['x', 'y']
    assert burger.split_comma_with_quotes('x,y,z,') == ['x', 'y', 'z']
    assert burger.split_comma_with_quotes(',x,y,z') == ['', 'x', 'y', 'z']
    assert burger.split_comma_with_quotes(',x,y,z,') == ['', 'x', 'y', 'z']

    # Test for normal behavior
    assert burger.split_comma_with_quotes('\nx') == ['\nx']
    assert burger.split_comma_with_quotes('\tx,y') == ['\tx', 'y']
    assert burger.split_comma_with_quotes('\rx,y,') == ['\rx', 'y']
    assert burger.split_comma_with_quotes('\n\rx,y,z,') == ['\n\rx', 'y', 'z']
    assert burger.split_comma_with_quotes(',x,y,z\t') == ['', 'x', 'y', 'z\t']
    assert burger.split_comma_with_quotes(',x,y,z\t,') == ['', 'x', 'y', 'z\t']

    # Test for quote behavior
    assert burger.split_comma_with_quotes('"x"') == ['"x"']
    assert burger.split_comma_with_quotes('"x","y"') == ['"x"', '"y"']
    assert burger.split_comma_with_quotes('"x",y,') == ['"x"', 'y']
    assert burger.split_comma_with_quotes("x,'y',z,") == ['x', "'y'", 'z']
    assert burger.split_comma_with_quotes(',x,y,"z"') == ['', 'x', 'y', '"z"']
    assert burger.split_comma_with_quotes(',x,"y,z",') == ['', 'x', '"y,z"']

    # Test for Exceptions
    try:
        burger.split_comma_with_quotes("'foo")
        assert 0
    except ValueError:
        pass
    try:
        burger.split_comma_with_quotes('"foo')
        assert 0
    except ValueError:
        pass
    try:
        burger.split_comma_with_quotes('"foo,bar')
        assert 0
    except ValueError:
        pass

########################################


def test_parse_csv():
    """
    Test burger.parse_csv()
    """

    # Test for normal behavior
    assert burger.parse_csv('x') == ['x']
    assert burger.parse_csv('x,y') == ['x', 'y']
    assert burger.parse_csv('x,y,') == ['x', 'y']
    assert burger.parse_csv('x,y,z,') == ['x', 'y', 'z']
    assert burger.parse_csv(',x,y,z') == ['', 'x', 'y', 'z']
    assert burger.parse_csv(',x,y,z,') == ['', 'x', 'y', 'z']

    # Test for normal behavior
    assert burger.parse_csv('\nx') == ['x']
    assert burger.parse_csv('\tx,y') == ['x', 'y']
    assert burger.parse_csv('\rx,y,') == ['x', 'y']
    assert burger.parse_csv('\n\rx,y,z,') == ['x', 'y', 'z']
    assert burger.parse_csv(',x,y,z\t') == ['', 'x', 'y', 'z']
    assert burger.parse_csv(',x,y,z\t,') == ['', 'x', 'y', 'z']

    # Test for quote behavior
    assert burger.parse_csv('"x"') == ['x']
    assert burger.parse_csv('"x","y"') == ['x', 'y']
    assert burger.parse_csv('"x",y,') == ['x', 'y']
    assert burger.parse_csv("x,'y',z,") == ['x', 'y', 'z']
    assert burger.parse_csv(',x,y,"z"') == ['', 'x', 'y', 'z']
    assert burger.parse_csv(',x,"y,z",') == ['', 'x', 'y,z']
    assert burger.parse_csv('x,"y""z",') == ['x', 'y"z']
    assert burger.parse_csv('x,\'y\'\'z\',') == ['x', 'y\'z']

    # Test for Exceptions
    try:
        burger.parse_csv("'foo")
        assert 0
    except ValueError:
        pass
    try:
        burger.parse_csv('"foo')
        assert 0
    except ValueError:
        pass
    try:
        burger.parse_csv('"foo,bar')
        assert 0
    except ValueError:
        pass

########################################


def test_translate_to_regex_match():
    """
    Test burger.translate_to_regex_match()
    """

    # Get an empty list
    assert not burger.translate_to_regex_match([])

    dir_list = burger.translate_to_regex_match(('foo.txt', '*.py'))
    assert dir_list

    # Find positive matches
    for item in dir_list:
        assert item('foo.txt') or item('a.py')
        assert not item('foo.bar')
        assert not item('py.px')
        assert not item('py')


########################################


def test_escape_xml_cdata():
    """
    Test burger.escape_xml_cdata()
    """

    tests = (
        ('before', 'before'),
        ('foo&foo', 'foo&amp;foo'),
        ('<token>', '&lt;token&gt;'),
        ('"quotes"\n', '"quotes"\n')
    )

    for test in tests:
        assert burger.escape_xml_cdata(test[0]) == test[1]


########################################


def test_escape_xml_attribute():
    """
    Test burger.escape_xml_attribute()
    """

    tests = (
        ('before', 'before'),
        ('foo&foo', 'foo&amp;foo'),
        ('<token>', '&lt;token&gt;'),
        ('"quotes"\n', '&quot;quotes&quot;&#10;'),
        ('\r\n\n\r', '&#10;&#10;&#10;'),
        ('mac\rstring', 'mac&#10;string'),
        ('linux\nstring', 'linux&#10;string'),
        ('pc\r\nstring', 'pc&#10;string'),
        ('test\ttabs\tnow', 'test&#09;tabs&#09;now')
    )

    for test in tests:
        assert burger.escape_xml_attribute(test[0]) == test[1]

########################################


def test_packed_paths():
    """
    Test burger.packed_paths()
    """

    tests = (
        ('test', 'test'),
        (('foo', 'bar'), 'foo;bar'),
        (['a', 'b', 'c'], 'a;b;c'),
        (['a','bart','c/c'], 'a;bart;c/c')
    )

    for test in tests:
        assert burger.packed_paths(test[0]) == test[1]

    # Test seperator replacement
    seperators = (
        ('a', ';', ':', '\n')
    )

    for sep in seperators:
        for test in tests:
            assert burger.packed_paths(test[0], seperator=sep) == test[1].replace(';', sep)

    # Test slashes and forced ending
    paths = (
        'c:\\foo\\bar',
        '/home/usr/bar',
        '~/.config',
        'foobar.txt',
        'c:\\foo\\bar\\',
        '/home/usr/bar/',
        '~/.config/',
        '/break\\me',
        '\\fun\\fun\\'
    )

    for path in paths:
        assert burger.packed_paths(path, slashes='/') == path.replace('\\', '/')
        assert burger.packed_paths(path, slashes='\\') == path.replace('/', '\\')

        temp = path.replace('\\', '/')
        if not temp.endswith('/'):
            temp = temp + '/'
        assert burger.packed_paths(path, slashes='/', force_ending_slash=True) == temp

        temp = path.replace('/', '\\')
        if not temp.endswith('\\'):
            temp = temp + '\\'
        assert burger.packed_paths(path, slashes='\\', force_ending_slash=True) == temp
