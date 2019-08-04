#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit tests for burger file functions

Copyright 2013-2019 by Rebecca Ann Heineman becky@burgerbecky.com

It is released under an MIT Open Source license. Please see LICENSE
for license details. Yes, you can use it in a
commercial title without paying anything, just give me a credit.
Please? It's not like I'm asking you for money!

"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import burger

########################################


def test_get_sdks_folder(tmpdir):
    """
    Test burger.get_sdks_folder()
    """

    saved = os.getenv('BURGER_SDKS', default=None)
    saved_dir = os.getcwd()

    # Test with current value
    if saved:
        assert burger.get_sdks_folder() == saved

    # Test folder override
    assert burger.get_sdks_folder(refresh=True, folder='test') == 'test'
    assert burger.get_sdks_folder() == 'test'

    # Test reading BURGER_SDKS
    os.environ['BURGER_SDKS'] = 'newvalue'
    assert burger.get_sdks_folder(refresh=True) == 'newvalue'
    assert burger.get_sdks_folder() == 'newvalue'

    # Test with fake 'sdks' folder

    os.environ.pop('BURGER_SDKS', None)
    tmpdir.mkdir('a')
    tmpdir.mkdir('a', 'b')
    tmpdir.mkdir('a', 'b', 'sdks')
    tmpdir.mkdir('a', 'b', 'sdks', 'c')
    tmpdir.mkdir('a', 'b', 'sdks', 'c', 'd')
    os.chdir(os.path.join(str(tmpdir), 'a', 'b', 'sdks', 'c', 'd'))
    assert burger.get_sdks_folder(refresh=True) == \
        os.path.join(str(tmpdir), 'a', 'b', 'sdks')

    # Cleanup
    os.chdir(saved_dir)
    tmpdir.remove()

    # Restore the cache to the correct value
    if saved:
        os.putenv('BURGER_SDKS', saved)
        burger.get_sdks_folder(refresh=True, folder=saved)

########################################


def test_get_path_ext():
    """
    Test burger.get_path_ext()
    """

    grouptuple = ('a', 'b', 'c', 'd')
    grouplist = ['a', 'b', 'c', 'd']
    teststr = os.pathsep.join(grouptuple)
    assert burger.get_path_ext(teststr) == grouplist
    assert burger.get_path_ext(grouptuple) == grouptuple
    assert burger.get_path_ext(grouplist) == grouplist

########################################


def test_make_exe_path():
    """
    Test burger.make_exe_path()
    """

    ran_test = False

    # Test for a known windows executable
    if os.getenv('SystemRoot', None):
        # Case insensitive test
        cmd = os.path.expandvars("${SystemRoot}\\System32\\cmd").lower()
        cmd_exe = cmd + '.exe'
        if os.path.isfile(cmd_exe):
            assert burger.make_exe_path(cmd).lower() == cmd_exe
            ran_test = True

    # Test with ls which is in the same place on Linux and macOS
    macls = '/bin/ls'
    if os.path.isfile(macls):
        assert burger.make_exe_path(macls) == macls
        ran_test = True

    # This has to come back false
    selffile = os.path.abspath(__file__)
    assert burger.make_exe_path(os.path.dirname(selffile)) is None

    # If this asserts, an executable test wasn't performed
    assert ran_test

########################################


def test_import_py_script():
    """
    Test burger.import_py_script()
    """

    selffile = os.path.dirname(os.path.abspath(__file__))

    # Load in from the 'a' folder
    sample = burger.import_py_script(
        os.path.join(selffile, 'data', 'sample.py'))
    assert sample.__name__ == 'sample'
    assert hasattr(sample, 'test')
    assert hasattr(sample, 'testa')
    assert not hasattr(sample, 'testb')
    assert sample.test() == 'sample_a'
    assert sample.testa() == 'testa'

    # Switch to the file in the 'b' folder
    sample = burger.import_py_script(
        os.path.join(selffile, 'data2', 'sample.py'))
    assert sample.__name__ == 'sample'
    assert hasattr(sample, 'test')
    assert not hasattr(sample, 'testa')
    assert hasattr(sample, 'testb')
    assert sample.test() == 'sample_b'
    assert sample.testb() == 'testb'

    # Test importing a with a unique module name
    sample = burger.import_py_script(
        os.path.join(selffile, 'data', 'sample.py'), 'hamster')
    assert sample.__name__ == 'hamster'
    assert hasattr(sample, 'test')
    assert hasattr(sample, 'testa')
    assert not hasattr(sample, 'testb')
    assert sample.test() == 'sample_a'
    assert sample.testa() == 'testa'

    assert not os.path.isfile(os.path.join(selffile, 'data', 'sample.pyc'))
    assert not os.path.isdir(os.path.join(selffile, 'data', '__pycache__'))
    assert not os.path.isfile(os.path.join(selffile, 'data2', 'sample.pyc'))
    assert not os.path.isdir(os.path.join(selffile, 'data2', '__pycache__'))

    # Intentionally fail to test the assert that fired
    sample = burger.import_py_script(os.path.join(selffile, 'doesntexist.py'))
    # File not found is the correct error
    assert sample is None

########################################


def test_run_py_script():
    """
    Test burger.run_py_script()
    """

    selffile = os.path.dirname(os.path.abspath(__file__))
    assert burger.run_py_script(
        os.path.join(selffile, 'data', 'sample.py'), 'test') == 'sample_a'
    assert burger.run_py_script(
        os.path.join(selffile, 'data', 'sample.py'), 'testa') == 'testa'

    assert burger.run_py_script(
        os.path.join(selffile, 'data2', 'sample.py'), 'test') == 'sample_b'
    assert burger.run_py_script(
        os.path.join(selffile, 'data2', 'sample.py'), 'testb') == 'testb'

    assert burger.run_py_script(
        os.path.join(
            selffile,
            'data',
            'sample.py'),
        'main',
        'gerbil') == 'gerbil'
    assert burger.run_py_script(
        os.path.join(
            selffile,
            'data2',
            'sample.py'),
        'main',
        'cat') == 'cattest'
