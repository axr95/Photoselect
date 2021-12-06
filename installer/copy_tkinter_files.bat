@ECHO off
FOR /F "delims=" %%A IN ('WHERE python') DO (
    SET PYPATH=%%~dA%%~pA
    GOTO :Copyfiles
)

:Copyfiles
XCOPY /E /I %PYPATH%\tcl lib
MKDIR pynsist_pkgs
COPY %PYPATH%\DLLs\_tkinter.pyd pynsist_pkgs
COPY %PYPATH%\DLLs\tcl86t.dll pynsist_pkgs
COPY %PYPATH%\DLLs\tk86t.dll pynsist_pkgs
COPY %PYPATH%\libs\_tkinter.lib pynsist_pkgs
