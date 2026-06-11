@echo off
REM Windows convenience wrapper — drag a folder onto this script,
REM or run: convert.bat "C:\path\to\your\docs"

if "%~1"=="" (
    echo Usage: convert.bat "source_folder" [optional_output_folder]
    echo.
    echo Drag a folder onto this script or pass the path as an argument.
    pause
    exit /b 1
)

python "%~dp0converter.py" %*
pause
