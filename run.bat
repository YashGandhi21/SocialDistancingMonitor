@ECHO OFF
:: This batch file runs the server on virtual environment
TITLE Execute Application
:: Assuming the virtual environment is set
ECHO Press Enter to activate venv
PAUSE
CALL venv\Scripts\activate.bat
ECHO Your current path is %cd%
where python
ECHO virtual environment is activated
ECHO Press Enter to start server
PAUSE
python app.py
ECHO Press Enter to deactivate
PAUSE
deactivate
ECHO Deactivated environment
ECHO Press Enter to exit
PAUSE
PAUSE