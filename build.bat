@echo off

echo Cleaning old build...
rmdir /s /q build
rmdir /s /q dist

echo Building...

pyinstaller --onefile --noconsole --name "TimerApp" main.py

echo.
echo Done!
pause