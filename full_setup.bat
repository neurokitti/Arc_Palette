@echo off
echo Cloning Arc Palette Repo...
git clone https://github.com/neurokitti/Arc_Palette.git
cd Arc_Palette
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
run.bat
pause
