@echo off
REM Activating the virtual environment (optional step)
call myenv\Scripts\activate

REM Running the Python script
python main.py

REM Deactivating the virtual environment (optional step)
deactivate
