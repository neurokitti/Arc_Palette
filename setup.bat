@echo off
echo Cloning Arc_API...
git clone https://github.com/neurokitti/Arc_API.git
echo creating venv... 
python -m venv .venv
echo activating venv... 
call .venv\Scripts\activate
echo installing requirments... 
pip install -r requirements.txt
pip install -r Arc_API\requirements-arc-api.txt

echo.
echo Installation complete! 
echo.
echo For best performance, please adjust your Windows settings:
echo - Wallpaper Settings: Set to "Stretch"
echo - Arc Theme: Set to "Mica"
echo - Theme: Set to "Transparent image"
echo.

pause
