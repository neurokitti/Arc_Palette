@echo off

:: Create a virtual environment
python -m venv myenv

:: Activate the virtual environment
call myenv\Scripts\activate

:: Install the required packages
pip install -r requirements.txt

:: Inform the user of the Windows settings recommendation
echo.
echo Installation complete! 
echo.
echo For best performance, please adjust your Windows settings:
echo - Wallpaper Settings: Set to "Stretch"
echo - Arc Theme: Set to "Mica"
echo - Theme: Set to "Transparent image"
echo.

:: Keep the command prompt open to display the message
pause
