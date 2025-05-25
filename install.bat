@echo off
echo Creating Python virtual environment (venv)...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Installation complete.
echo To run the app, activate the venv (venv\Scripts\activate) and then run: python app.py
pause
