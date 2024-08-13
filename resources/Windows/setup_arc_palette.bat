@echo off

REM .bat files change directory, need to open to directory where script launched from
cd "%~dp0"

REM Go to repo's root directory where everything is setup
cd ..\..

echo Cloning Arc_API...
git clone https://github.com/neurokitti/Arc_API.git
echo creating venv...
python -m venv .venv
echo activating venv...
call .venv\Scripts\activate
echo installing requirements...
pip install -r requirements.txt
pip install -r Arc_API\requirements-arc-api.txt

echo.
echo Installation complete!


pause
