WSL, Cygwin, MSYS support
=========================

Burger for Python supports the Windows Subsystem for Linux (WSL), Cygwin and MSYS2 when attempting to execute or locate tools in the underlying Windows host. One of the main issues is the varied ways a Linux pathname is mapped to Windows.

When `burger.strutils` is loaded, it will perform tests to determine which python platform it's running under and will enable specialized code or run tools to properly handle pathname conversion. For WSL, the tool used is `wslpath` and for Cygwin and MSYS2 the tool is `cygpath`.

Pathname examples
-----------------

If the path for windows looks like this, `C:\Windows\Notepad.exe`, it will look like this on these platforms.

- WSL `/mnt/c/Windows/Notepad.exe`
- Cygwin `/cygdrive/c/Windows/Notepad.exe`
- MSYS2 `/c/Windows/Notepad.exe`

Pathname translation
--------------------

If the `burger` library is running under WSL, Cygwin or MSYS2, the function `wslwinreg.convert_to_windows_path()` will convert a Linux style path into a Windows path and `wslwinreg.convert_from_windows_path()` will convert from a Windows path to a Linux style path. If burger is not running under these environments, these pathname translators will return the input without modification.

Environment flags
-----------------

The flag is set to `True` if `burger` is running on the named platform, otherwise it will be `False`.

- `burger.strutils.IS_MACOSX`
- `burger.strutils.IS_WINDOWS`
- `burger.strutils.IS_LINUX`
- `burger.strutils.IS_CYGWIN`
- `burger.strutils.IS_MSYS`
- `burger.strutils.IS_WSL`

`burger.strutils.IS_WINDOWS_HOST` is `True` if the platform can execute Windows executables natively (Without Wine).

PATHEXT
-------

`PATHEXT` is an environment variable present on Windows systems that presents a list of acceptable suffixes for executables. `burger.buildutils.get_path_ext()` will obtain the list of extensions available taking into account the differences of MSYS2, Cygwin, WSL and Windows. This function will return an empty list for macOS and Linux. WSL is a special case, since both native Linux and Windows .exe files can be executed, so the list will only have the suffixes for Windows executables.
