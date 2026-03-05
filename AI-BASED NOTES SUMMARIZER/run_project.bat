@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting SmartStudyHub...
python app.py
pause