@echo off

REM .bat files change directory, need to open to directory where script launched from
cd "%~dp0"

REM Check if Python 3 is installed
powershell.exe -c "if ($(python -V) -like 'Python 3.*') { return $true } else { throw $false }" >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python 3 is not installed. Please install Python 3.8 or higher and try again.  PYTHON DOWNLOAD: https://www.python.org/downloads/release/python-3125/
    pause
    exit /b
)

echo Downloading Arc Palette Repo...
curl -L https://github.com/neurokitti/Arc_Palette/archive/refs/heads/main.zip -o Arc_Palette.zip
echo Unzipping Arc Palette...
tar -xf Arc_Palette.zip
rename Arc_Palette-main Arc_Palette
echo Deleting Arc Palette ZIP file...
del Arc_Palette.zip

cd Arc_Palette

echo Downloading Arc_API...
curl -L https://github.com/neurokitti/Arc_API/archive/refs/heads/main.zip -o Arc_API.zip
echo Unzipping Arc_API...
tar -xf Arc_API.zip
rename Arc_API-main Arc_API
echo Deleting Arc_API ZIP file...
del Arc_API.zip

echo Creating venv...
python -m venv .venv
echo Activating venv...
call .venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt
pip install -r Arc_API\requirements-arc-api.txt

echo.
echo Installation complete!
echo.
.\resources\Windows\run_arc_palette.bat
pause
