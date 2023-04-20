@echo off

echo Installing required libraries...
pip install -r requirements.txt

echo.
echo Initializing the database...
cd src
set FLASK_APP=app.py

echo.
flask db init
flask db migrate
flask db upgrade

echo.
echo Starting the server...
flask run
