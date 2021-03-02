Data type validators
====================

These classes are used in conjunction with a python class definition to create class attributes that will throw an exception if invalid data was stored. It allows for ensuring that data stored in these attributes are of only the type desired.

- `burger.validators.BooleanProperty`
- `burger.validators.IntegerProperty`
- `burger.validators.StringProperty`
- `burger.validators.StringListProperty`
- `burger.validators.EnumProperty`
- `burger.validators.NoneProperty`

How to use
----------

They are implemented as class immutable attributes with a member variable definition. It is preferred to use an underscore as the first character of the attribute to denote it is a hidden variable.

```python
# Class with validated attributes
from burger.validators import *

class foo(object):

    # _bool_var is the class instance storage name
    bool_var = BooleanProperty('_bool_var')

    # Note the name can be any variable, but the use
    # of an alternate name may be an invitation for
    # its direct use and bypassing the validator
    int_var = IntegerProperty('int_var2')

    def __init__(self):
        # Set defaults
        self.bool_var = True

        # This will throw an exception due to
        # validation failure
        # self.bool_var = 'string'

        self.int_var = 42


a = foo()
# Will set to False
a.bool_var = False
# Will set to True (Due to 9 being non zero)
a.bool_var = 9
# Will set to False
a.bool_var = 'False'
# Will throw an exception
a.bool_var = 'foobar'
# Will set to None
a.bool_var = None

# Will set to 8675309
a.int_var = 8675309
# Will set to 13
a.int_var = '13'
# Will throw an exception
a.int_var = 'USA USA'

# Will bypass the validators and set the values to strings
a._bool_var = 'NSA NSA'
a.int_var2 = 'USA USA'
```
