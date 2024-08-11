@echo off

python -m venv myenv

call myenv\Scripts\activate

pip install -r requirements.txt

echo.
echo Installation complete! 
echo.
echo For best performance, please adjust your Windows settings:
echo - Wallpaper Settings: Set to "Stretch"
echo - Arc Theme: Set to "Mica"
echo - Theme: Set to "Transparent image"
echo.

pause
