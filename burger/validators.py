#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Package that contains class member validators

@package burger.validators
"""

# pylint: disable=no-name-in-module,too-few-public-methods
# pylint: disable=consider-using-f-string
# pylint: disable=deprecated-class

from numbers import Number

# Try the Python 3 import
try:
    from collections.abc import Iterable
except ImportError:
    # Try the Python 2 import
    from collections import Iterable

from .strutils import string_to_bool, is_string, UNICODE as unicode, \
    LONG as long

# Note: (object) is required for python 2.7 compatiblity
# pylint: disable=useless-object-inheritance


class Property(object):
    """
    Base Class to create enforced types

    Attributes:
        _name: The real name of the class instance
    """

    def __init__(self, name):
        """Initialize to default
        Args:
            name: Name of the instance storage index
        """

        self._name = name

    def __get__(self, instance, owner=None):
        """Return value

        Args:
            instance: Reference to object containing data
            owner: Not used

        Returns:
            None, or verified data
        """

        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        """Set the string value

        Args:
            instance: Reference to object containing data
            value: None or value the can be converted to bool
        """

        instance.__dict__[self._name] = value

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

    def __set__(self, instance, value):
        """Set the boolean value

        Args:
            instance: Reference to object containing data
            value: None or value the can be converted to bool

        Exception:
            ValueError on invalid input.

        See Also:
            strutils.string_to_bool
        """

        if value is not None:
            # Convert to bool
            value = string_to_bool(value)

        # Boolean value
        instance.__dict__[self._name] = value

########################################


class IntegerProperty(Property):
    """Class to enforce 64 bit integer in variable

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

    def __set__(self, instance, value):
        """Set the integer value

        Args:
            instance: Reference to object containing data
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
                            value = long(value, 0)
                        # Try again as a float
                        except ValueError:
                            value = float(value)
                    else:
                        raise ValueError(
                            'Value "{}" is not a number'.format(value))

                # value is a number, bounds check it
                if value < -0x8000000000000000 or value > 0x7fffffffffffffff:
                    raise ValueError(
                        'Value "{}" must fit in signed 64 bits'.format(value))

                # Ensure it's an int()
                value = long(value)

        # Integer value
        instance.__dict__[self._name] = value

########################################


class StringProperty(Property):
    """Class to enforce string in member variable

Example:
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to "foo"'
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

'Print True'
f.x = True
print(f.x)
    """

    def __set__(self, instance, value):
        """Set the string value
        Args:
            instance: Reference to object containing data
            value: None or value the can be converted to bool
        """
        if value is not None:
            # Convert to string
            if not is_string(value):
                value = unicode(value)

        # String value
        instance.__dict__[self._name] = value


########################################


class StringListProperty(Property):
    """Class to enforce string list in member variable

Example:
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to ["foo"]'
    x = StringListProperty('foo')
    'Init to None'
    y = StringListProperty()
    'Init to ["a","b","c"]'
    z = StringListProperty(["a","b","c"])

'Create the class'
f = foo()

'Print ["foo"]'
print(f.x)

'Print ['False']
f.x = 'False'
print(f.x)

'Print True'
f.x = True
print(f.x)
    """

    def __get__(self, instance, owner=None):
        """Return value

        Args:
            instance: Reference to object containing data
            owner: Not used

        Returns:
            None, or verified data
        """

        # If never initialized, create an empty list
        result = instance.__dict__.get(self._name, None)
        if result is None:
            result = []
            # Make sure the value is set to the empty list
            instance.__dict__[self._name] = result
        return result

    def __set__(self, instance, value):
        """Set the string value
        Args:
            instance: Reference to object containing data
            value: None or value the can be converted to bool
        """

        if value is None:
            value = []
        else:
            # Convert to string
            if is_string(value) or not isinstance(value, Iterable):
                value = [unicode(value)]
            else:
                value = [unicode(i) for i in value]

        # String list value
        instance.__dict__[self._name] = value


########################################


class EnumProperty(Property):
    """
    Class to enforce string list in member variable

Attributes:
    _enums: Enumeration dictionary

Example:
j = (('a', 'b', 'c'), 'd', 'e', ['f', 'g', 'h'], 'i')
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to 0'
    x = EnumProperty(j, "a")
    'Init to 0'
    y = EnumProperty(j)
    'Init to 4'
    z = EnumProperty(j, "i")

'Create the class'
f = foo()

'Print 0'
print(f.x)

'Print 2
f.x = 'g'
print(f.x)

'Print 2'
f.x = 'h'
print(f.x)
    """

    def __init__(self, name, enums):
        """Initialize to default
        Args:
            name: Name of the instance storage index
            enums: list of enumeration strings
        """

        self._enums = enums

        if not isinstance(enums, Iterable):
            raise ValueError(
                'enums "{}" is not an iterable'.format(enums))

        if is_string(enums):
            raise ValueError(
                'enums "{}" can not be a string'.format(enums))

        # Set the initial value using the derived class
        Property.__init__(self, name)

    def __set__(self, instance, value):
        """Set the string value
        Args:
            instance: Reference to object containing data
            value: None or value the can be converted to bool
        """

        if value is not None:
            if isinstance(value, Number):
                if value < 0:
                    raise ValueError(
                        'Value "{}" is less than zero'.format(value))
                if value >= len(self._enums):
                    raise ValueError(
                        'Value {} is greater than or equal to {}'.format(
                            value, len(self._enums)))
                value = int(value)
            else:
                # Check for an override
                enums = instance.__dict__.get(
                    self._name + '_enums', self._enums)

                # Convert to string
                for i, item in enumerate(enums):
                    if isinstance(item, Iterable):
                        if value in item:
                            value = i
                            break
                    if item == value:
                        value = i
                        break
                else:
                    raise ValueError(
                        'Value "{}" is not found in the list "{}"'.format(
                            value, enums))

        # String list value
        instance.__dict__[self._name] = value

########################################


class NoneProperty(object):
    """
    Class to enforce None in member variable

Attributes:
    _name: The real name of the class instance

Example:
'Inherit from (object) for Python 2.7'
>>> class foo(object):
    'Init to None'
    x = NoneProperty()

'Create the class'
f = foo()

'Print None'
print(f.x)

'Exception on non None data'
f.x = 'not None'
Traceback (most recent call last):
    ...
ValueError: Not None value
    """

    def __init__(self, name):
        """Initialize to default
        Args:
            name: Name of the instance storage index
        """

        self._name = name

    def __get__(self, instance, owner=None):
        """Return None

        Args:
            instance: Reference to object containing data
            owner: Not used

        Returns:
            None, or verified data
        """

        return None

    def __set__(self, instance, value):
        """Throw if not None

        Args:
            instance: Reference to object containing data
            value: None or value the can be converted to bool
        """

        if value is not None:
            raise ValueError(
                '"{}" can only be set to None, not "{}"'.format(
                    self._name, value))
        instance.__dict__[self._name] = value
