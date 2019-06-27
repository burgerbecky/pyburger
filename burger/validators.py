#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains class member validators
"""

## \package burger.validators

from numbers import Number

from .strutils import string_to_bool, is_string, PY2

# Note: (object) is required for python 2.7 compatiblity
# pylint: disable=useless-object-inheritance


class Property(object):
    """Base Class to for enforced types """

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
        """Set the string value
        Args:
            obj: Not used
            value: None or value the can be converted to bool
        """
        self._value = value

    def __delete__(self, obj):
        """Delete the bool
        Args:
            obj: Not used
        """
        self._value = None

########################################


class BooleanProperty(Property):
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

########################################


class IntegerProperty(Property):
    """Class to enforce integer in member variable

Example:
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to 1'
    x = IntegerProperty(1.0)
    'Init to 55'
    y = IntegerProperty('55')
    'Init to None'
    z = IntegerProperty()

'Create the class'
f = foo()

'Print 1'
print(f.x)

'Print 0'
f.x = False
print(f.x)

'f.x is set to 99 with string'
f.x = '99.00'
print(f.x)

'Exception on bad write'
f.x = 'not boolean'
Traceback (most recent call last):
    ...
ValueError: Not integer value
    """

    def __set__(self, obj, value):
        """Set the integer value
        Args:
            obj: Not used
            value: None or value the can be converted to bool
        Exception:
            ValueError on invalid input.
        See Also:
            strutils.string_to_bool
        """
        if value is not None:
            # Bool is a special case (0,1)
            if isinstance(value, bool):
                value = int(value)
            else:
                # Not a number?
                if not isinstance(value, Number):

                    # Convert string to integer
                    if is_string(value):
                        # Convert to integer
                        try:
                            if PY2:
                                value = long(value, 0)
                            else:
                                value = int(value, 0)
                        # Try again as a float
                        except ValueError:
                            value = float(value)
                    else:
                        raise ValueError(
                            "Value {} can't convert to a number".format(value))
                # Verify the number is in range for an integer
                if value < -0x8000000000000000 or value > 0x7fffffffffffffff:
                    raise ValueError(
                        'Value {} must fit in signed 64 bits'.format(value))
                if PY2:
                    value = long(value)
                else:
                    value = int(value)
        self._value = value

########################################


class StringProperty(Property):
    """Class to enforce string in member variable

Example:
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to false'
    x = StringProperty('foo')
    'Init to None'
    y = StringProperty()

'Create the class'
f = foo()

'Print foo'
print(f.x)

'Print False'
f.x = 'False'
print(f.x)

'Print True
f.x = True
print(f.x)
    """

    def __set__(self, obj, value):
        """Set the string value
        Args:
            obj: Not used
            value: None or value the can be converted to bool
        """
        if value is not None:
            # Convert to string
            if not is_string(value):
                if PY2:
                    # pylint: disable=undefined-variable
                    value = unicode(value)
                else:
                    value = str(value)
        self._value = value
