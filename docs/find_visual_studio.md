# Searching for Visual Studio

The function `burger.windowsutils.find_visual_studios()` will return a list of `burger._vsinstance.WindowsSDKInstance` and `burger._vsinstance.VisualStudioInstance` objects. This function will work on Windows, Cygwin, MSYS2 and Windows Subsystem for Linux. Other platforms will return an empty list.

## VisualStudioInstance

``name`` will be one of these entries.

- Microsoft Visual Studio .NET 2003
- Microsoft Visual Studio 2005
- Microsoft Visual Studio 2008
- Microsoft Visual Studio 2010
- Microsoft Visual Studio 2012
- Microsoft Visual Studio 2013
- Microsoft Visual Studio 2015
- Microsoft Visual Studio 2017
- Microsoft Visual Studio 2019

``version`` will be a string in the form of "16.8.30907.101"

``version_info`` is a tuple in the form of (16, 8, 30907, 101). This is most useful in doing a numeric version comparison.

``path`` is the root path of the copy of Visual Studio such as "C:\Program Files (x86)\Microsoft Visual Studio 14.0"

``known_paths`` is a dict with full pathnames of a executable. A suffix is needed to denote the requested CPU. The suffixes are \_x86, \_x64, \_arm and \_arm64.

Note: If the key is missing, the binary, such as ``msbuild.exe`` may not be available or installed in that version of Visual Studio.

- ``devenv.exe_x86`` =  "c:\Program Files (x86)\Microsoft Visual Studio .NET 2003\Common7\IDE\devenv.exe"
- ``vcvarsall.bat`` = "c:\Program Files (x86)\Microsoft Visual Studio .NET 2003\Common7\Tools\vsvars32.bat"
- ``cl.exe_x86`` = "c:\Program Files (x86)\Microsoft Visual Studio .NET 2003\Vc7\bin\cl.exe"
- ``link.exe_x86`` = "c:\Program Files (x86)\Microsoft Visual Studio .NET 2003\Vc7\bin\link.exe"
- ``lib.exe_x86`` = "c:\Program Files (x86)\Microsoft Visual Studio .NET 2003\Vc7\bin\lib.exe"
- ``msbuild.exe_x86`` "C:\Program Files (x86)\MSBuild\14.0\bin\msbuild.exe"

---

## WindowsSDKInstance

``name`` will be one of these entries.

- Windows 5 SDK
- Windows 6 SDK
- Windows 7 SDK
- Windows 8 SDK
- Windows 10 SDK

``version`` will be a string in the form of "10.0.10150.0"

``version_info`` is a tuple in the form of (10, 0, 10150, 0). This is most useful in doing a numeric version comparison. The first number will match the actual SDK version such as 5, 6, 7, 8 or 10.

``path`` is the root path of the copy of Visual Studio such as "C:\Program Files (x86)\Windows Kits\8.0" or "C:\Program Files (x86)\Microsoft SDKs\Windows\v7.0A"

``known_paths`` is a dict with full pathnames of a folder, library or executable. A suffix is needed to denote the requested CPU. The suffixes are \_x86, \_x64, \_arm and \_arm64.

Note: If the key is missing, the binary, such as ``signtool.exe`` may not be available or installed in that version of Visual Studio.

### Folders

- ``WinSDK.ucrt`` = "C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\ucrt"
- ``WinSDK.um`` = "C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\um"
- ``WinSDK.shared`` = "C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\shared"
- ``WinSDK.winrt`` = "C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\winrt"
- ``WinSDK.cppwinrt`` == "C:\Program Files (x86)\Windows Kits\10\Include\10.0.18362.0\cppwinrt"

### Library folders

- ``WinSDK.libucrt_x86`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\ucrt\x86"
- ``WinSDK.libucrt_x64`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\ucrt\x64"
- ``WinSDK.libucrt_arm`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\ucrt\arm"
- ``WinSDK.libucrt_arm64`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\ucrt\arm64"
- ``WinSDK.lib_x86`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\um\x86"
- ``WinSDK.lib_x64`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\um\x64"
- ``WinSDK.lib_arm`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\um\arm"
- ``WinSDK.lib_arm64`` = "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.18362.0\um\arm64"

### Executables

- ``rc.exe_x86`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\rc.exe"
- ``rc.exe_x64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\rc.exe"
- ``rc.exe_arm64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\arm64\rc.exe"
- ``signtool.exe_x86`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\signtool.exe"
- ``signtool.exe_x64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\signtool.exe"
- ``signtool.exe_arm`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\arm\signtool.exe"
- ``signtool.exe_arm64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\arm64\signtool.exe"
- ``makecat.exe_x86`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\makecat.exe"
- ``makecat.exe_x64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\makecat.exe"
- ``makecat.exe_arm64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\arm64\makecat.exe"
- ``midl.exe_x86`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\midl.exe"
- ``midl.exe_x64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\midl.exe"
- ``midl.exe_arm64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\arm64\midl.exe"
- ``mc.exe_x86`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\mc.exe"
- ``mc.exe_x64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\mc.exe"
- ``mc.exe_arm64`` = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\arm64\mc.exe"
