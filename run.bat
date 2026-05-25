@echo off
echo ========================================================
echo        AI-Based Autonomous Navigation System
echo ========================================================

:: Check if Pygame dependencies are installed (Silent fallback)
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required libraries...
    pip install -r requirements.txt
)

echo.
echo [1] Launching Flask API Telemetry Server...
start "SYS.NAV Dashboard Server" cmd /c "python app.py"

echo [2] Giving the server a moment to boot...
timeout /t 3 /nobreak >nul

echo [3] Launching Web Browser Dashboard...
python -m webbrowser "http://127.0.0.1:5000/"

echo [4] Booting Virtual Simulation Environment (Pygame)...
python virtual_simulation.py

echo.
echo Closing systems...
pause
