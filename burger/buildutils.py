#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains build helper functions

@package burger.buildutils

@var burger.buildutils._BURGER_SDKS_FOLDER
Cached location of the BURGER_SDKS folder

@var burger.buildutils._WINDOWS_ENV_PATHS
Environment variable locations of window applications
"""

# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-with
# pylint: disable=import-error
# pylint: disable=deprecated-module

from __future__ import absolute_import, print_function, unicode_literals

import os
import platform
import subprocess
import sys
import errno

try:
    from wslwinreg import convert_from_windows_path
except ImportError:
    def convert_from_windows_path(x):
        """
        For platforms that don't have this function
        don't remap
        """
        return x

from .strutils import is_string, encapsulate_path, get_windows_host_type, \
    get_mac_host_type, PY3_3_OR_HIGHER, PY3_5_OR_HIGHER, IS_CYGWIN, \
    IS_MSYS, IS_WSL, IS_WINDOWS, IS_WINDOWS_HOST

# Cached location of the BURGER_SDKS folder
_BURGER_SDKS_FOLDER = None

# Environment variable locations of window applications
_WINDOWS_ENV_PATHS = [
    "ProgramFiles",
    "ProgramFiles(x86)"
]

# For some goofy reason, Cygwin converts ProgramFiles
# into uppercase and preforms case sensitive comparisons
# To get around this, do the conversion for this table
if IS_CYGWIN or IS_MSYS:
    _WINDOWS_ENV_PATHS[0] = _WINDOWS_ENV_PATHS[0].upper()

########################################


def _create_header_guard(filename):
    """
    Create the header guard.

    Create the header guard by taking the filename,
    converting to upper case and replacing spaces and
    periods with underbars.

    Args:
        filename: Pathname of the file to generate a header guard.
    Returns:
        Base name, capitalized, and with underscores.
    """

    headerguard = os.path.basename(filename).upper()
    headerguard = headerguard.replace(" ", "_")
    return "__{}__".format(headerguard.replace(".", "_"))

########################################


def get_sdks_folder(verbose=False, refresh=False, folder=None):
    """
    Return the path of the BURGER_SDKS folder

    If the environment variable BURGER_SDKS is set,
    return the pathname it contains. Otherwise,
    print a warning if verbose is True and then attempt to find
    the "sdks" folder by traversing the current working directory
    for a folder named "sdks". If one isn't found, return None.

    Examples:
        # Normal use
        sdksfolder = burger.buildutils.get_sdks_folder()
        if not sdksfolder:
            print("failure")
            raise NameError("sdks not found, set BURGER_SDKS")

        # Alert the user if BURGER_SDKS isn't set
        burger.buildutils.get_sdks_folder(verbose=True)

        # Force the use of a supplied folder for sdks
        burger.buildutils.get_sdks_folder(refresh=True, folder="./foo/sdks/")

    Args:
        verbose: If True, print a message if BURGER_SDKS was not present
        refresh: If True, reset the cache and force a reload.
        folder: Path to use as BURGER_SDKS in the cache as an override

    Returns:
        None if the environment variable is not set, or the
        value of BURGER_SDKS.
    """

    global _BURGER_SDKS_FOLDER  # pylint: disable=global-statement

    # Clear the cache if needed
    if refresh:
        _BURGER_SDKS_FOLDER = None

    # Set the override, if found
    if folder:
        _BURGER_SDKS_FOLDER = folder

    # Not cached?
    if _BURGER_SDKS_FOLDER is None:

        # Load from the system
        _BURGER_SDKS_FOLDER = os.getenv("BURGER_SDKS", default=None)

        # Test for None or empty string
        if _BURGER_SDKS_FOLDER:
            _BURGER_SDKS_FOLDER = convert_from_windows_path(
                _BURGER_SDKS_FOLDER)

        else:
            # Warn about missing environment variable
            if verbose:
                print("The environment variable \"BURGER_SDKS\" is not set")

            # pylint: disable=import-outside-toplevel
            # Try to find the directory in the current path
            from .fileutils import traverse_directory
            sdks = traverse_directory(os.getcwd(), "sdks",
                                      find_directory=True, terminate=True)
            if sdks:
                _BURGER_SDKS_FOLDER = sdks[0]
                if verbose:
                    print(
                        "Assuming {} is the BURGER_SDKS folder".format(
                            sdks[0]))

    return _BURGER_SDKS_FOLDER

########################################


def fix_csharp(csharp_application_path):
    """
    Convert pathname to execute a C# exe file.

    @details C# applications can launch as is on Windows platforms,
    however, on Mac OSX and Linux, it must be launched
    from mono. Determine the host machine and if not
    windows, automatically prepend "mono" to
    the application's name to properly launch it

    This will also encase the name in quotes in case there are
    spaces in the pathname

    Args:
        csharp_application_path: Pathname string to update

    Returns:
        List of commands for the platform to launch a C# application.
    """

    # Prepend mono on non-windows systems
    if not get_windows_host_type(True):
        return ["mono", encapsulate_path(csharp_application_path)]
    return [csharp_application_path]

########################################


def is_exe(exe_path):
    """
    Return True if the file is executable

    Note:
        Windows platforms don't support the "x" bit so all
        files are executable if they exist.

    Args:
        exe_path: Full or partial pathname to test for existance
    Returns:
        True if the file is executable, False if the file doesn't exist or
        is not valid.
    """
    return os.path.isfile(exe_path) and os.access(exe_path, os.X_OK)

########################################


def get_path_ext(pathext=None):
    """
    Return a list of executable extensions

    If pathext is None, query the environment variable PATHEXT and
    return the entries as a string list. If pathext is a string,
    parse it as if it was a system specific PATHEXT string and
    if it's an iterable, return the value as is. If PATHEXT doesn't exist
    or is empty, return an empty list.

    Windows usually sets the value like this
    ``PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC``

    Args:
        pathext: String parsed as PATHEXT, iterable returned as is
    Returns:
        List of file name extension strings.
    See Also:
        burger.buildutils.make_exe_path, burger.buildutils.find_in_path
    """

    # Read the environment variable?
    if pathext is None:
        pathext = os.getenv("PATHEXT", None)
        if pathext is None:
            if IS_WSL:
                # Special case for WSL targets, allow .exe files
                return [".EXE"]
            return []

    # If a string, or environment variable?
    if is_string(pathext):
        # Special case for Cygwin, since os.pathsep
        # is ":" but the environment variable uses
        # ";" from Windows
        separator = ";" if IS_CYGWIN or IS_MSYS else os.pathsep
        # Parse the string
        pathext = pathext.split(separator)

    # Return the list or iterable
    return pathext

########################################


def make_exe_path(exe_path, pathext=None):
    """
    Given a folder and a executable name, return the true absolute path

    Examples:
        # exe could be returned as exe, exe.exe, exe.cmd, etc...
        path = make_exe_path("C:\\code\\exe")
        if path is None:
            print("No file named exe at C:\\code")

    Note:
        On macOS and Linux, PATHEXT is not set, this is for supporting
        extension types for common batch files or other executable extensions.

    Args:
        exe_path: Path of the executable to test
        pathext: Extension list to test
    Returns:
        None if a match was not found, or a full pathname with extension.

    See Also:
        burger.buildutils.get_path_ext, burger.buildutils.find_in_path
    """

    test_list = [exe_path]

    # Get the extension list
    pathext = get_path_ext(pathext)
    if pathext:
        # Only convert to lower case once
        exe_path_lower = exe_path.lower()

        # Does the file already have an extension?
        if not any(exe_path_lower.endswith(temp.lower()) for temp in pathext):
            # Create a list of possible file names with extensions
            test_list = [exe_path + temp for temp in pathext]

    # Try all the extensions (Can be an empty list)
    for temp_path in test_list:
        if is_exe(temp_path):
            break
    else:
        temp_path = None
    return temp_path

########################################


def find_in_path(filename, search_path=None, executable=False):
    """
    Using the system PATH environment variable, search for a file

    If the flag executable is False, the file will be found using a
    simple path search. If the flag is True, the file will be searched
    for using the extensions in the PATHEXT environment variable in
    addition to use the filename as is.

    If search_path is a string, it will be seperated using os.pathsep. If
    not, it will be treated as an interable list of strings of full pathnames
    to search. If it is None, the PATH environment variable will be used.

    Examples:
        # Can return "doxygen", "doxygen.exe" or "doxygen.com" depending
        # on what was found
        burger.find_in_path("doxygen", executable=True)

        # Will only find "foo.txt"
        burger.find_in_path("foo.txt")

    Args:
        filename: File to locate
        search_path: Search paths to use instead of PATH
        executable: True to ensure it's an executable
    Return:
        None if not found, a full path if the file is found.

    See Also:
        burger.buildutils.get_path_ext, burger.buildutils.make_exe_path
    """

    # pylint: disable=too-many-branches

    # Set up for added standard extentions
    test_list = [filename]
    if executable:

        # Are there path extensions (Windows)?
        pathext = get_path_ext()
        if pathext:

            # Only convert to lower case once
            filename_lower = filename.lower()

            # Does the file already have an extension?
            if not any(filename_lower.endswith(item.lower())
                       for item in pathext):
                # Create a list of possible file names with extensions
                test_list = [filename + item for item in pathext]

                # If Linux, allow "" as an extension
                if not IS_WINDOWS and IS_WINDOWS_HOST:
                    test_list.append(filename)

    # Is there a search path override?
    if not search_path:
        # Use the environment variable
        paths = os.getenv("PATH", "")
        if not paths:
            paths = os.defpath
    else:
        paths = search_path

    if is_string(paths):
        # Break it up based on the path separator
        paths = paths.split(os.pathsep)

    # On windows platforms, the current directory takes
    # precedence
    if search_path is None and get_windows_host_type(True):
        paths.insert(0, os.getcwd())

    # Scan the list of paths to find the file
    tested = set()
    for path in paths:
        # Normalize the path
        path = os.path.normcase(path)

        # Skip duplicates
        if path not in tested:
            tested.add(path)

            for item in test_list:
                temp_path = os.path.join(path, item)

                # Perform the test as an exe
                if executable:
                    if is_exe(temp_path):
                        break
                # Test for just a file
                elif os.path.isfile(temp_path):
                    break
            else:
                continue
            return os.path.normcase(os.path.normpath(temp_path))

    # Not found in the loops
    return None

########################################


def expand_and_verify(file_string):
    """
    Expand the input string with os.path.expandvars()

    After expanding the string, test for the existence of the file
    and return the expanded path if True. Otherwise, return None

    Examples:
        perforcepath = burger.expand_and_verify("${PERFORCE}\\p4.exe")
        if perforcepath is None:
            return

    Args:
        file_string: Pathname with environment variable tokens

    Returns:
        None if the string couldn't be expanded or if the file didn't exist,
            otherwise, return the expanded pathname

    """

    result_path = os.path.expandvars(file_string)
    if result_path is not None:
        result_path = convert_from_windows_path(result_path)
        if not os.path.isfile(result_path):
            result_path = None
    return result_path

########################################


def run_command(args, working_dir=None, quiet=False, capture_stdout=False,
                capture_stderr=False):
    """
    Execute a program and capture the return code and text output.

    Pass a command line formatted for the current shell and then this
    function will execute that command and capture both stdout and stderr if
    desired.

    Note:
        The first parameter is passed to subprocess.Popen() as is.

    Args:
        args: List of command line entries, starting with the program pathname
        working_dir: Directory to set before executing command
        quiet: Set to True if errors should not be printed
        capture_stdout: Set to True if stdout is to be captured
        capture_stderr: Set to True if stderr is to be captured
    Returns:
        The return error_code, stdout, stderr
    """

    # Which output streams are to be captured?
    stdout = subprocess.PIPE if capture_stdout else None
    stderr = subprocess.PIPE if capture_stderr else None

    # Set the working directory if needed
    old_directory = os.getcwd()
    if working_dir:
        os.chdir(working_dir)

    try:
        tempfp = subprocess.Popen(args, cwd=working_dir, stdout=stdout,
                                  stderr=stderr, universal_newlines=True)
    except OSError as error:
        if not quiet:
            if is_string(args):
                msg = args
            else:
                msg = " ".join(args)
            print("Command line \"{}\" generated error {}".format(msg, error))

        # Restore directory
        os.chdir(old_directory)
        return (error.errno, "", "")

    # Restore directory
    os.chdir(old_directory)

    stdoutstr, stderrstr = tempfp.communicate()
    return (tempfp.returncode, stdoutstr, stderrstr)

########################################


def is_codewarrior_mac_allowed():
    """
    Return True if this machine can run Codewarrior for Mac OS Carbon.

    Test first if the host platform is a mac, and if so, test if it's
    capable of running Mac OS Carbon Codewarrior 9 or 10

    Returns:
        True if CodeWarrior for Mac OS can be run on this Macintosh

    See Also:
        strutils.host_machine
    """

    # Test if a mac

    if get_mac_host_type():
        # Get the Mac OS version number
        mac_ver = platform.mac_ver()
        release = mac_ver[0]

        # Convert 10.5.8 to 10.5

        digits = release.split(".")

        # Snow Leopard (10.6) supports Rosetta
        # Lion (10.7) and Mountain Lion (10.8) do not

        if float(digits[0]) >= 10:
            if float(digits[1]) < 7:
                return True

    # Can't run, not a mac or Power PC native or emulation isn't supported
    return False

########################################


def import_py_script(file_name, module_name=None):
    """
    Manually load in a python file.

    Load in a python script from disk and parse it, creating
    a .pyc file if needed and reading from a .pyc file if it exists.

    Note:
        The module returned will not be present in the sys.modules cache, this
        is by design to allow python files with the same name to be loaded
        from different directories without creating a cache collision

    Args:
        file_name: Name of the file to load
        module_name: Name of the loaded module for ``__name__``
    Returns:
        The imported python script object
    See Also:
        run_py_script
    """

    # pylint: disable=import-outside-toplevel
    # pylint: disable=too-many-branches

    # If there's no module name, glean one from the filename
    if not module_name:
        module_name = os.path.splitext(os.path.split(file_name)[-1])[0]

    old_dont = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        if PY3_5_OR_HIGHER:

            # Python 3.5 and allows the loading of a module without
            # touching the cache
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                module_name, file_name)

            # File not found?
            if not spec:
                result = None
            else:
                # Import and then execute
                result = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(result)

        else:
            # First step, if there's a module already loaded by this
            # name, save it for restoration later

            saved = None
            if module_name in sys.modules:
                saved = sys.modules[module_name]
                del sys.modules[module_name]

            # Perform the load, throw exception on error
            try:
                if PY3_3_OR_HIGHER:
                    # Python 3.3 and 3.4 prefers using the SourceFileLoader
                    # class
                    from importlib.machinery import SourceFileLoader
                    # pylint: disable=deprecated-method
                    result = SourceFileLoader(
                        module_name, file_name).load_module(None)

                else:
                    # Use the imp library for Python 2.x to 3.2
                    import imp  # type: ignore
                    result = imp.load_source(module_name, file_name)

            # Wrap up by restoring the cache the way it was found
            finally:
                if saved:
                    sys.modules[module_name] = saved
                else:
                    # Remove the generated entry since load_source() added it

                    # Note: Test before deletion, in case load_source threw
                    # an exception before creating the entry
                    if module_name in sys.modules:
                        del sys.modules[module_name]

    except IOError as error:
        # File not found is the correct error
        if error.errno == errno.ENOENT:
            result = None
        else:
            raise

    finally:
        sys.dont_write_bytecode = old_dont

    return result

########################################


def run_py_script(file_name, function_name=None, arg=None):
    """
    Manually load and run a function in a python file.

    Load in a python script from disk and execute a specific function.
    Returns the value returned from the loaded script.

    Note:
        The script will not be added to the module cache.

    Args:
        file_name: Name of the file to load
        function_name: Name of the function in the file to call
        arg: Argument to pass to the function
    Returns:
        The value returned from the python script.
    See Also:
        import_py_script
    """

    # If a function name wasn't passed, assume it's ``main``
    if not function_name:
        function_name = "main"

    # Load in the script
    module = import_py_script(file_name)

    # Find the function and execute it
    method = getattr(module, function_name)
    if arg is None:
        return method()
    return method(arg)

# pylint: disable=redefined-builtin


def execfile(filename, globals, locals=None):
    """
    Implementation of execfile from Python 2

    It's not exact. This version requires a globals object.

    To maintain compatilibity to execfile() in python 2, the
    input parameters are hard coded to filename, globals,
    and locals despite what pylint insists on.

    Args:
        filename: Full path of python file to load and execute
        globals: Usually globals()
        locals: Optional, usually locals()

    Returns:
        None
    """

    # pylint: disable=exec-used

    # If no locals are passed, use the globals
    if locals is None:
        locals = globals

    # Read in the python file
    with open(filename, "rb") as inputfile:
        source = inputfile.read()

    # Compile to byte code
    bytecode = compile(source, filename, "exec")
    exec(bytecode, globals, locals)
