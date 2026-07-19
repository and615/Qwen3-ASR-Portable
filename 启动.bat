@echo off
cd /d "%~dp0"
echo ====================================
echo   Qwen3-ASR Speech Recognition
echo ====================================
echo.
echo Working Directory: %cd%
echo.
echo Starting Web Interface...
echo Please visit: http://localhost:7860
echo.
python\python.exe webui.py
pause