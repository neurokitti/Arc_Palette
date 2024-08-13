@echo off

:: Check if Python is installed
powershell.exe -c "$(python -V) -like 'Python 3.*'"
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.6 or higher and try again.
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
rd /s /q Arc_Palette-main

cd Arc_Palette

echo Downloading Arc_API...
curl -L https://github.com/neurokitti/Arc_API/archive/refs/heads/main.zip -o Arc_API.zip
echo Unzipping Arc_API...
tar -xf Arc_API.zip
rename Arc_API-main Arc_API
echo Deleting Arc_API ZIP file...
del Arc_API.zip
rd /s /q Arc_API-main

echo Creating venv... 
python -m venv .venv
echo Activating venv... 
call .venv\Scripts\activate

echo Installing requirements... 
Pip3 install -r requirements.txt
Pip3 install -r Arc_API\requirements-arc-api.txt

echo.
echo Installation complete! 
echo.
run.bat
pause



