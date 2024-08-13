@echo off

REM .bat files change directory, need to open to directory where script launched from
cd "%~dp0"

REM Go to repo's root directory where everything is setup
cd ..\..

REM Activating the virtual environment (optional step)
call .venv\Scripts\activate

REM Running the Python script
python main.py

REM Deactivating the virtual environment (optional step)
deactivate
