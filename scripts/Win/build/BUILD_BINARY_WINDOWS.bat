@echo off

REM .bat files change directory, need to open to directory where script launched from
cd "%~dp0"

REM Launch the PowerShell script
where pwsh.exe
IF %ERRORLEVEL% NEQ 0 (
  echo Please install PowerShell 7 or newer, as is required to build for Windows.
  echo Easiest way is to run the following command: winget install Microsoft.PowerShell
  exit 1
)
pwsh.exe -ExecutionPolicy Bypass -File .\BUILD_BINARY_WINDOWS.ps1
