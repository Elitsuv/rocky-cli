@echo off
echo ========================================================
echo Rocky CLI - Installation Script
echo ========================================================
echo.
echo Installing dependencies and Rocky CLI tool...
echo.

pip install .

echo.
echo ========================================================
echo Installation Complete!
echo You can now use Rocky CLI from any terminal by typing:
echo rocky
echo.
echo To start a focus session right away, type:
echo rocky focus 25
echo ========================================================
pause
