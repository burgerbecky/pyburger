True or False
=============

These set of functions are used to convert a value that resolves to `True` or `False` to the words "True" or "False". However, due to the need for some output streams to require a specific form of case, these functions will output the strings according to these rules. The function burger.strutils.string_to_bool() is helpful in converting a larger number of strings and numbers into a boolean.

burger.strutils.truefalse() outputs "true" or "false"

burger.strutils.TRUEFALSE() outputs "TRUE" or "FALSE"

burger.strutils.TrueFalse() outputs "True" or "False"

True False code example
-----------------------

```python

# Prints "true"
print(burger.strutils.truefalse(True))

# Prints "FALSE"
print(burger.strutils.TRUEFALSE(False))

# Prints "True"
print(burger.strutils.TrueFalse(True))

# Prints "True"
t = burger.strutils.string_to_bool(1.34)
print(burger.strutils.TrueFalse(t))

```
