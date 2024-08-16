@echo off

REM .bat files change directory, need to open to directory where script launched from
cd "%~dp0"

REM Launch the PowerShell script
powershell.exe -ExecutionPolicy Bypass -File .\BUILD_BINARY_WINDOWS.ps1
