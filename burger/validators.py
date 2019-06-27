#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains class member validators
"""

## \package burger.validators

from .strutils import string_to_bool

# Note: (object) is required for python 2.7 compatiblity
# pylint: disable=useless-object-inheritance

########################################

class BooleanProperty(object):
    """Class to enforce bool in member variable

See Also:
    strutils.string_to_bool

Example:
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to false'
    x = BooleanProperty(False)
    'Init to true'
    y = BooleanProperty(True)
    'Init to None'
    z = BooleanProperty()

'Create the class'
f = foo()

'Print True'
print(f.x)

'Print False'
f.x = False
print(f.x)

'f.x is set to bool False with string'
f.x = 'False'
print(f.x)

'Exception on bad write'
f.x = 'not boolean'
Traceback (most recent call last):
    ...
ValueError: Not boolean value
    """

    def __init__(self, value=None):
        """Initialize to default
        Args:
            value: Initial value, must be None or bool
        """
        ## Boolean value
        self._value = None
        self.__set__(None, value)

    def __get__(self, obj, objtype=None):
        """Return value

        Args:
            obj: Not used
            objtype: Not used
        Returns:
            None, or bool
        """
        return self._value

    def __set__(self, obj, value):
        """Set the boolean value
        Args:
            obj: Not used
            value: None or value the can be converted to bool
        Exception:
            ValueError on invalid input.
        See Also:
            strutils.string_to_bool
        """
        if value is not None:
            # Convert to bool
            value = string_to_bool(value)
        self._value = value

    def __delete__(self, obj):
        """Delete the bool
        Args:
            obj: Not used
        """
        self._value = None
