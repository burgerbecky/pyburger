#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains setup.py helper functions

Functions to generate setup.py

@package burger.setuputils

@var burger.setuputils._SETUP_URL_LIST
Homepage urls in order of precedence

@var burger.setuputils._PROJECT_KEYWORDS
Keywords to process in project dict

@var burger.setuputils._PROJECT_REMAP
Keywords to remap for project dict to setup.py

@var burger.setuputils._SETUPTOOLS_KEYWORDS
Keywords to process in setuptools dict

@var burger.setuputils._SETUPTOOLS_REMAP
Keywords to remap for setuptools dict to setup.py
"""

# pylint: disable=consider-using-f-string
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-arguments

from __future__ import absolute_import, print_function, unicode_literals

from .strutils import is_string, convert_to_array

from .fileutils import save_text_file

# A toml reader is needed but it's not standard until python 3.11
try:
    # Python 3.11 or higher? Use the default
    import tomllib
except ImportError:
    try:
        # Try the library tomllib is based on
        import tomli as tomllib  # type: ignore
    except ImportError:
        try:
            # If using python 2.7-3.4, use this old library
            import toml as tomllib  # type: ignore
        except ImportError:
            print("Error: Install toml for Python 2 or tomli for Python 3")


# Homepage urls in order of precedence
_SETUP_URL_LIST = ("Homepage",
                   "Documentation",
                   "Source")


# Keywords to process in project dict
_PROJECT_KEYWORDS = (
    "name",
    "version",
    "description",
    "author",
    "author_email",
    "license",
    "requires-python",
    "dependencies",
    "classifiers",
    "keywords"
)

# Keywords to remap for project dict to setup.py
_PROJECT_REMAP = {
    "requires-python": "python_requires",
    "dependencies": "install_requires",
}

# Keywords to process in setuptools dict
_SETUPTOOLS_KEYWORDS = (
    "platforms",
    "zip-safe"
)

# Keywords to remap for setuptools dict to setup.py
_SETUPTOOLS_REMAP = {
    "zip-safe": "zip_safe"
}


########################################


def _output_entry(lines, key, data, tabs="    ", tabs2="        "):
    """
    Create an entry for a python dict

    Given a list of entries, a data key, and the data, determine how to output
    the data and append the lines to the lines stream

    Tabs can either be a string or a number. If a number, it's multipied by
    space and that is the string inserted into the line entrie(s)

    Args:
        lines: list of lines for final output
        key: dict key to generate
        data: data attached to the dict key
        tabs: indentation
        tabs2: secondary indentation for list entries
    """

    # If tabs is a number, convert to a string
    if not is_string(tabs):
        tabs = " " * tabs
    if not is_string(tabs2):
        tabs2 = " " * tabs2

    # Is the data a string?
    if is_string(data):
        line = "{}\"{}\": \"{}\",".format(tabs, key, data)
        lines.append(line)

    # Bools don't get quoted
    elif isinstance(data, bool):
        line = "{}\"{}\": {},".format(tabs, key, str(data))
        lines.append(line)

    # Lists
    else:
        # Start the list
        line = "{}\"{}\": [".format(tabs, key)
        lines.append(line)

        # Insert all entries in the list
        for entry in data:
            line = "{}\"{}\",".format(tabs2, entry)
            lines.append(line)

        # Close the list
        lines.append(tabs + "],")

########################################


def _setup_dynamic(project, tool):
    """
    Process the dynamic variables in pyproject.toml

    Scan the project dict for a "dynamic" entry, and if one exists, parse the
    tool dict for those entries and copy them directly into the project dict.

    This will modify the project dict with the parsed data, and in some cases
    file loaded data.

    Note:
        At this time, only ``attr`` is supported. ``file`` support to be added
        later

    Args:
        project: "project" dict entry from the toml file
        tool: "tool" dict entry from the toml file
    """

    # Sanity check
    if not project or not tool:
        return

    # See if there's a setuptools in the tools record
    setuptools = tool.get("setuptools")
    if not setuptools:
        return

    # See if there is a dynamic entry
    dynamic_dir = setuptools.get("dynamic")
    if not dynamic_dir:
        return

    # At this point, it's good to go

    # Is there a dynamic entry?
    dynamic = project.get("dynamic")
    if dynamic:

        # Iterate over the entries
        for item in dynamic:

            # Only attr and file matter
            entries = dynamic_dir[item]

            # Process file entry (Higher priority)
            record = entries.get("file")
            if record:
                print("file not supported yet ")
                continue

            # Check for attribute
            record = entries.get("attr")
            if record:
                # Split the attribute
                record = record.strip().split(".")

                # Get the attribute name from the list
                attr_name = record.pop()

                # Rejoin the list to get the import name
                module_name = ".".join(record)

                # If it's just the attibute, use __init__
                # as the module
                module_name = module_name or "__init__"

                # Load the module
                module = __import__(module_name)

                # Obtain the attribute
                record = getattr(module, attr_name, None)

                # Insert into the project
                if record:
                    project[item] = record

########################################


def _setup_process_entries(lines, project, keyword_list,
                           remap=None, tabs="    ", tabs2="        "):
    """
    Handle the list of common entries

    Iterate over the keyword list on the dict ``project``. All matching entries
    are then sent to _output_entry() for output. Keywords are remapped via the
    remap table so that keys that are for pyproject.toml are remapped to keys
    suitable for setup.py

    Args:
        lines: list of lines for final output
        project: dict of data from the toml file
        keyword_list: List of keywords to scan
        remap: List of keywords to swap to alternate keywords
        tabs: indentation
        tabs2: secondary indentation for list entries

    See Also:
        _output_entry
    """

    # Sanity check
    if not project:
        return

    # If there's no remap object, ensure the get() call works
    if not remap:
        remap = {}

    # Iterate over the supported keywords
    for item in keyword_list:

        # Valid data?
        data = project.get(item)
        if data is not None:

            # Remap the key if needed
            key = remap.get(item, item)

            # Output the data
            _output_entry(lines, key, data, tabs, tabs2)

########################################


def _setup_find_url(lines, project):
    """
    Locate the most likely URL for the homepage

    Check for which URL is found using the list setuputils._SETUP_URL_LIST.
    The first one found will be marked at the setup.py homepage.

    Args:
        lines: list of lines for final output
        project: dict of data from the toml file
    """

    # Is there a urls entry?
    urls = project.get("urls")
    if urls:

        # Scan in priority order
        for item in _SETUP_URL_LIST:

            # Found one?
            url = urls.get(item)
            if url:
                break
        else:
            # Grab the first one on the list as a fallback
            url = next(iter(urls.values()))

        # Sanity check
        if url:
            # Add the url entry
            _output_entry(lines, "url", url)

########################################


def _setup_find_license_file(lines, project):
    """
    Degrade license-files to license_file

    pyproject.toml supports multiple license files, setup.py supports
    only one. Use the first license file.

    Args:
        lines: list of lines for final output
        project: dict of data from the toml file
    """

    # Is there a license-files entry?
    files = project.get("license-files")
    if files:
        # This hack is simple, take the first file
        _output_entry(lines, "license_file", files[0])

########################################


def _setup_find_readme_file(lines, project):
    """
    Insert the readme file into the metadata

    Since this loads a file a compile time, a code snippet is inserted
    into the setup.py file that generates a global variable called
    ``LONG_DESCRIPTION``. This variable is used to set the entry
    ``long_description``.

    Args:
        lines: list of lines for final output
        project: dict of data from the toml file
    """

    # Is there a readme file?
    readme = project.get("readme")
    if readme:

        # Insert the import needed for the code fragments
        index = lines.index("import setuptools")
        lines[index:index] = [
            "import io",
            "import os"
        ]

        # Insert the reader
        index = lines.index("SETUP_ARGS = {") - 1
        lines[index:index] = [
            "# Ensure the working directory is captured",
            "CWD = os.path.dirname(os.path.abspath(__file__))",
            "",
            "# Read the file into LONG_DESCRIPTION using utf-8",
            ("with io.open(os.path.join(CWD, \"{}\")"
             ", encoding=\"utf-8\") as fp:").format(readme),
            "    LONG_DESCRIPTION = fp.read()",
            ""
        ]

        # Insert the entry to the end of the list
        lines.append("    \"long_description\": LONG_DESCRIPTION,")

########################################


def _setup_find_packages(lines, setuptools_entry):
    """
    Find the entries ``packages`` and ``package_data``

    Args:
        lines: list of lines for final output
        setuptools_entry: dict of data from the toml file
    """

    # Are there packages?
    packages = setuptools_entry.get("packages")
    if packages:
        packages = packages.get("find")
        if packages:
            packages = packages.get("include")
            if packages:
                packages = convert_to_array(packages)
                _output_entry(lines, "packages", packages)

    # Are there package data?
    package = setuptools_entry.get("package-data")
    if package:

        # Header for package_data
        lines.append("    \"package_data\": {")

        # Create entries for the nested dict
        for item in package:
            # item is the key, package[item] is the data
            _output_entry(lines, item, package[item], 8, 12)

        # Footer for package_data
        lines.append("    },")

########################################


def create_setup_py(toml_name=None, setup_name=None):
    """
    Create a setup.py for setuptools

    The latest setuptools uses pyproject.toml for all the settings, but
    wheels packaged this way don't properly install using older versions of pip.

    To get around this issue, a setup.py file is generated from the data in
    pyproject.toml for inclusion of the distributed wheel, so python 2.7's
    version of pip can still properly install the python module

    Args:
        toml_name: Name of the pyproject.toml file. Default is pyproject.toml
        setup_name: Name of the setup.py file. Default is setup.py
    """

    # Assume defaults
    if not toml_name:
        toml_name = "pyproject.toml"

    if not setup_name:
        setup_name = "setup.py"

    # Generated lines, start with the default header
    lines = [
        "#!/usr/bin/env python",
        "# -*- coding: utf-8 -*-",
        "",
        "\"\"\"",
        "Generated with burger.create_setup_py()",
        "\"\"\"",
        "",
        "import setuptools",
        "",
        "# Data lovingly ripped off from a toml file",
        "SETUP_ARGS = {",
    ]

    # Start by parsing the toml file
    with open(toml_name, "rb") as fp:
        pyproject = tomllib.load(fp)

    # Get the two dicts of interest
    project = pyproject.get("project")
    tool = pyproject.get("tool")

    # If there is no project dict, abort
    if project:

        # Find the setuptools entry in tools
        if tool:
            setuptools_entry = tool.get("setuptools", None)
        else:
            setuptools_entry = None

        # Handle dynamic lookups
        # This has to be first, since it updates
        # the project dict
        _setup_dynamic(project, tool)

        # Process the simple entries
        _setup_process_entries(lines, project,
                               _PROJECT_KEYWORDS, _PROJECT_REMAP)
        _setup_process_entries(lines, setuptools_entry,
                               _SETUPTOOLS_KEYWORDS, _SETUPTOOLS_REMAP)

        # Handle the special case for url
        _setup_find_url(lines, project)

        # Find the license file
        _setup_find_license_file(lines, project)

        # Find the readme file
        _setup_find_readme_file(lines, project)

        # Handle the packages
        _setup_find_packages(lines, setuptools_entry)

    # Wrap it up with a footer
    lines.extend([
        "}",
        "",
        "# Pass metadata to pip for old python versions",
        "",
        "if __name__ == \"__main__\":",
        "    setuptools.setup(**SETUP_ARGS)"
    ])

    # Output the setup.py file
    save_text_file(setup_name, lines)
