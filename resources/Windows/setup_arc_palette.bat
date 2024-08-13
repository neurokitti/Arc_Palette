@echo off

REM .bat files change directory, need to open to directory where script launched from
cd "%~dp0"

REM Go to repo's root directory where everything is setup
cd ..\..

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


pause
